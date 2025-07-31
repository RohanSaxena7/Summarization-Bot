# 🧵 LangChain Summarization Bot

An intuitive, multi-source summarization app built with **LangChain**, **Groq's Gemma2-9b LLM**, and **Streamlit**. Summarize content from smaller YouTube videos, webpages, PDFs, or CSV files — by providing links and uploading files. The assistant extracts, processes, and summarizes the content conversationally.

**App Link**: _[Your Streamlit App Link Here]_

## 🚀 Features

- 🎥 **YouTube Summarization:**
Extracts subtitles/captions using `pytubefix` for reliable video transcript processing.
- 🌐 **Webpage Summarization:**
Summarizes any URL with extracted textual content.
- 📄 **PDF and CSV File Support:**
Upload files directly and get concise summaries without system dependencies like Poppler.
- 🤖 **LLM-Powered Summarization:**
Integrates Groq’s Gemma2-9b-It model via LangChain for accurate, fluent summaries.
- 💡 **Advanced Chain Types:**
Uses LangChain’s built-in `refine` summarization chain for automatic chunking and summarization prompting.
- 🔐 **Secure API and Secrets Handling:**
Manage Groq API keys and LangSmith tracking tokens securely via Streamlit secrets or sidebar input.


## 📦 Requirements

Before running or deploying, ensure you have:

- **Python 3.10.x** (recommended: 3.10.17 for Streamlit compatibility)
- **pip** (Python package manager)
- **Groq API Key** ([Sign up here](https://console.groq.com))
- (Optional for local dev) `.env` file or Streamlit secrets for keys
- Poppler is **not required** (using `PyPDFLoader` makes PDF loading simpler in cloud environments)


## 🏗️ How It Works

1. **User launches the app** locally or on Streamlit Cloud.
2. **Upload a PDF or CSV file**, or paste a YouTube/video/webpage URL.
3. **Provide your Groq API Key** in the sidebar.
4. The app extracts the text (including YouTube subtitles using `pytubefix`).
5. **LangChain’s `map_reduce` summarization chain** splits, summarizes chunks, and composes a final summary using Groq’s LLM.
6. The summarized output is shown conversationally on the web interface.

## 📝 Usage Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure your secrets:**

- Locally, add a `.streamlit/secrets.toml` file with:

```toml
LANGCHAIN_API_KEY="your_groq_api_key_here"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT="Summarization Bot"
```

- On Streamlit Cloud, add the same keys in the “Secrets” section.

4. **Run the app:**
```bash
streamlit run app.py
```

5. **On the web app:**

- Upload files or paste URLs/YouTube video URLs.
- Enter your API key if not set in secrets.
- Click “Summarize the content” and receive your summary.


## ⚙️ Configuration

- **requirements.txt**

```
streamlit
langchain
langchain-community
langchain_groq
pytubefix
pypdf
unstructured
validators
python-dotenv
```

- **Streamlit Secrets:**

```toml
LANGCHAIN_API_KEY="your_groq_api_key"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT="Summarization Bot"
```

- **Python version:** 3.10.17 recommended for best compatibility.


## 🧩 LangSmith Tracing (Optional)

- Enables detailed logging and trace visualization on [LangSmith](https://console.langchain.com).
- Simply set the above environment variables (`LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2`, `LANGCHAIN_PROJECT`) to activate tracing.
- Summarizes prompt and output data for audit and debugging purposes.


## 🖥️ Sample User Flow

1. **Open app** and either upload a PDF or CSV or paste a URL/YouTube video link.
2. **Enter Groq API key** in the sidebar or Streamlit secrets.
3. **Click 'Summarize the content'** to trigger summarization.
4. **View the concise summary** presented instantly in the UI.

## ❓ FAQ

**Why doesn’t the YouTube URL always work?**

- The app uses `pytubefix` to reliably extract captions.
- Some videos may have no subtitles available, so they cannot be summarized.

**Is my API key secure?**

- Yes! Keys are never hardcoded and can be safely managed with Streamlit secrets.

**Why does PDF summarization work without Poppler?**

- This app uses `PyPDFLoader` which does not require external tools like Poppler, making it cloud-friendly.

**Can I customize the summarization prompts?**

- The app uses LangChain’s built-in `refine` chain with default prompts for simplicity and robustness.


## 📚 Resources

- [Groq API Signup](https://console.groq.com)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Streamlit Documentation](https://docs.streamlit.io)
- [LangSmith Tracing](https://console.langchain.com)

