import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from pytubefix import YouTube
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, UnstructuredURLLoader, UnstructuredCSVLoader
#YoutubeLoader has an issue right now
import tempfile
import os

#Langchain Tracking
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]

# Streamlit app
st.set_page_config(page_title="LangChain: Summarize Youtube URLs, CSV, or PDFs", page_icon="🧵")
st.title("SummarizeBot: Summarize Youtube Videos, Webpages, PDF files or CSV Files")
st.subheader('Summarize URLs, PDFs or CSVs')

# API Key input
with st.sidebar:
    groq_api_key = st.text_input("Please enter your Groq API Key", value="", type="password")

# User input
generic_url = st.text_input("Paste a Youtube or Website URL", key="url_input")
file = st.file_uploader("Upload a PDF or CSV file", type=['pdf', 'csv'])

#We dont need this part in map_reduce, it does the prompting on its own, we only need it for stuffdocument chain
# Prompt
# prompt_template = """
# Provide a summary of the following content:
# Content: {text}
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

#To load youtube captions from pytubefix
def get_youtube_transcript(url):
    try:
        yt = YouTube(url)
        captions = yt.captions
        if captions:
            en_caption = captions.get_by_language_code('en')
            if en_caption:
                return en_caption.generate_srt_captions()
            else:
                for cap in captions.all():
                    return cap.generate_srt_captions()
        return None
    except Exception as e:
        st.error(f"Failed to retrieve YouTube transcript: {e}")
        return None

#to load pdf,csv files
def load_document_from_file(uploaded_file):
    if uploaded_file is None:
        return None
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    try:
        # Use appropriate loader based on file type
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)
        elif uploaded_file.name.endswith(".csv"):
            loader = UnstructuredCSVLoader(tmp_path)
        else:
            return None
        documents = loader.load()
    finally:
        os.unlink(tmp_path)  # Clean up the temp file
    return documents

if st.button("Summarize the content"):
    if not groq_api_key.strip():
        st.error("Please provide your Groq API key.")
    elif (not generic_url.strip()) and (not file):
        st.error("Please provide a URL or upload a file.")
    else:
        try:
            with st.spinner("Processing...⌛"):
                docs = None
                loader = None
                # PRIORITY: File upload over URL
                if file is not None:
                    docs = load_document_from_file(file)
                elif generic_url.strip():
                    if not validators.url(generic_url):
                        st.error("Please enter a valid URL.")
                        st.stop()
                    if 'youtube.com' in generic_url or 'youtu.be' in generic_url:
                        # Use your custom function here to get transcript text
                        transcript_text = get_youtube_transcript(generic_url)
                        if not transcript_text:
                            st.error("No captions found for this YouTube video.")
                            st.stop()
                        # Wrap transcript in a Document object list
                        docs = [Document(page_content=transcript_text)]
                    else:
                        loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                       headers= {
                                                                    "User-Agent": (
                                                                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_0) "
                                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                        "Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
                                                                    ),
                                                                    "Accept-Language": "en-US,en;q=0.9",
                                                                    "Accept-Encoding": "gzip, deflate, br"
                                                                }
                        )
                        if loader is not None:
                            docs = loader.load()
                        else:
                            st.error("Failed to initialize the document loader.")
                            st.stop()
                if not docs:
                    st.error("Could not load content from the provided source.")
                    st.stop()
                #api_key
                llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
                # Summarization
                chain = load_summarize_chain(llm= llm, chain_type="refine") #we do NOT need prompt for this, map rduce does it itself
                output_summary = chain.run(docs)
                st.success(output_summary)
        except Exception as e:
            err_msg = str(e)
            if ("Request too large" in err_msg or "rate_limit_exceeded" in err_msg or "TPM" in err_msg or "'code': 'rate_limit_exceeded'" in err_msg):
                st.error("Sorry, this video or website is too long to summarize. Please try a shorter input or select a smaller section of content.")
            else:
                st.exception(f"Exception: {e}")

