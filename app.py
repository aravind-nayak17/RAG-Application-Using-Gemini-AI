import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from google import genai   # ✅ new SDK

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# -------------------- LOAD ENV --------------------
load_dotenv()


# -------------------- PDF TEXT --------------------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    return text


# -------------------- CHUNKING --------------------
def get_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return splitter.split_text(text)


# -------------------- VECTOR STORE --------------------
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.from_texts(chunks, embedding=embeddings)
    db.save_local("faiss_index")


def load_vector_store():
    if not os.path.exists("faiss_index"):
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )


# -------------------- GEMINI (NEW SDK) --------------------
def ask_gemini(context, question):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",   # ✅ from your working list
        contents=f"""
Answer ONLY using the context below.
Do NOT repeat the context.

Context:
{context}

Question:
{question}

If not found, say:
Answer is not available in the context.
"""
    )

    return response.text.strip()


# -------------------- QUERY --------------------
def handle_query(question):
    db = load_vector_store()

    if db is None:
        st.error("Upload and process PDF first.")
        return

    docs = db.similarity_search(question, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    answer = ask_gemini(context, question)

    st.markdown("### Answer:")
    st.markdown(answer)


# -------------------- MAIN --------------------
def main():
    st.set_page_config(page_title="Gemini RAG")
    st.header("Chat with PDF using Gemini💁x")

    question = st.text_input("Ask a question")

    if question:
        handle_query(question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True
        )

        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Upload at least one PDF")
                return

            with st.spinner("Processing..."):
                text = get_pdf_text(pdf_docs)
                chunks = get_chunks(text)
                create_vector_store(chunks)

                st.success("Done")


if __name__ == "__main__":
    main()