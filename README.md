# Chat with PDF using Gemini 💁

A RAG (Retrieval-Augmented Generation) app that lets you upload PDFs and ask questions about them using Google Gemini and FAISS vector search.

## How it works

1. Upload one or more PDF files via the sidebar
2. Click **Submit & Process** — the app extracts text, splits it into chunks, and stores embeddings in a local FAISS index
3. Ask any question in the text box — the app retrieves the most relevant chunks and sends them to Gemini for an answer

## Tech Stack

| Layer | Library |
|---|---|
| UI | Streamlit |
| PDF parsing | PyPDF2 |
| Text splitting | LangChain `RecursiveCharacterTextSplitter` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| Vector store | FAISS (local) |
| LLM | Google Gemini 2.5 Flash (`google-genai` SDK) |

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Run the app

```bash
streamlit run app.py
```

## Requirements

Create a `requirements.txt` with:

```
streamlit
python-dotenv
PyPDF2
google-genai
langchain
langchain-community
langchain-text-splitters
faiss-cpu
sentence-transformers
huggingface-hub
```

## Project Structure

```
.
├── app.py              # Main application
├── .env                # API key (not committed)
├── .gitignore
├── requirements.txt
└── faiss_index/        # Auto-generated after first PDF upload
```

## .gitignore

Make sure to add these to `.gitignore`:

```
.env
faiss_index/
__pycache__/
*.pyc
```

## Notes

- The FAISS index is saved locally and persists between sessions. Re-upload and reprocess if you want to switch document sets.
- Answers are strictly grounded in the uploaded PDF content — the model will say so if the answer isn't found.
- Embedding is done locally (no API cost) using the MiniLM model from HuggingFace.
