```markdown
# RAG Application Using Gemini AI

A simple Streamlit app that implements a Retrieval-Augmented Generation (RAG) workflow using Google (Gemini) generative models and FAISS for vector search. Upload PDF documents, the app extracts text, splits it into chunks, creates embeddings using Google Generative AI, stores them in a FAISS index, and answers user questions grounded in the PDF content using a chat model.

> Note: This project uses Google Generative AI (Gemini) via the langchain_google_genai integration. Access to Google Generative AI models and the appropriate API key is required.

## Features

- Upload multiple PDF files through a Streamlit UI.
- Extract text from PDFs using PyPDF2.
- Split text into chunks with langchain's RecursiveCharacterTextSplitter.
- Generate embeddings with GoogleGenerativeAIEmbeddings.
- Store embeddings in a local FAISS index for fast similarity search.
- Use ChatGoogleGenerativeAI (Gemini) to answer user questions using retrieved context.
- Simple, minimal UI for experimentation.

## Prerequisites

- Python 3.8+ (recommend 3.10+)
- Google account / project with access to Google Generative AI and a valid API key
- Enough disk space for FAISS index files

## Required environment variables

Create a `.env` file in the project root with:

```
GOOGLE_API_KEY=your_google_api_key_here
```

The project reads the API key using python-dotenv.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/aravind-nayak17/RAG-Application-Using-Gemini-AI.git
cd RAG-Application-Using-Gemini-AI
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Install dependencies:

There may not be a pinned requirements file in the repo. Install the packages used in the script:

```bash
pip install streamlit PyPDF2 python-dotenv langchain langchain_google_genai google-generativeai faiss-cpu
```

Note: Depending on your platform and Python version, you might use `faiss` or `faiss-cpu`. Adjust accordingly.

## Usage

1. Ensure `.env` contains your `GOOGLE_API_KEY`.
2. Start the Streamlit app:

```bash
streamlit run python_script
```

(If the file has a `.py` extension or your local file is named `python_script.py`, run `streamlit run python_script.py`.)

3. Open the Streamlit UI in your browser (Streamlit will show the local URL).
4. In the sidebar, upload one or more PDF files and click "Submit & Process".
5. When processing completes, ask questions in the input box; the app will query the FAISS index and use Gemini to answer from the retrieved context.

## How it works (high level)

1. PDF upload -> text extraction (PyPDF2).
2. Text is split into overlapping chunks using RecursiveCharacterTextSplitter to preserve context.
3. Each chunk is embedded with GoogleGenerativeAIEmbeddings.
4. Embeddings are stored locally in FAISS (`faiss_index` folder).
5. For user queries, the FAISS index performs a similarity search to retrieve relevant chunks.
6. Retrieved chunks are passed to ChatGoogleGenerativeAI (a Gemini model) via langchain's question answering chain to produce the final answer.

## Important configuration & model notes

- Embedding model: the script uses `models/embedding-001`. Ensure your Google Generative AI access includes this or change to your available embedding model name.
- Chat model: the script references `"gemini-pro"` as the model in ChatGoogleGenerativeAI. Use a model you have access to or update accordingly.
- FAISS index location: the script saves/loads FAISS data from a local folder `faiss_index` — make sure the app has write/read permissions.

## Troubleshooting & common fixes

- If the app does not start, verify the correct entrypoint file name. The repository contains a file named `python_script` (no `.py`), so run `streamlit run python_script` or rename it to `python_script.py`.
- Bug in the example script: the Python entrypoint is written as:
  ```python
  if _name_ == "_main_":
      main()
  ```
  This should be corrected to:
  ```python
  if __name__ == "__main__":
      main()
  ```
- If you get permission or API errors from Google, confirm your `GOOGLE_API_KEY` is valid and has the required permissions for Generative AI endpoints.
- If FAISS fails to install on your platform, try `pip install faiss-cpu` or consult FAISS installation docs for your OS.

## Security considerations

- Do not commit your `GOOGLE_API_KEY` to source control. Use `.env` and add `.env` to `.gitignore`.
- Uploaded PDFs and the generated FAISS index may contain sensitive information. Treat stored data accordingly and remove it when no longer needed.

## Example .env

```
GOOGLE_API_KEY=AIza...
```

## Contributing

Contributions, bug reports, and improvements are welcome. If you propose changes, please:

1. Fork the repo.
2. Create a branch for your change.
3. Open a pull request with a clear description.

## License

Specify your preferred license (e.g., MIT). Add a `LICENSE` file if you choose an open-source license.

## Acknowledgements

- Streamlit for the UI.
- LangChain for the text processing and chains.
- Google Generative AI (Gemini) for embeddings and chat capabilities.
- FAISS for vector similarity search.
```