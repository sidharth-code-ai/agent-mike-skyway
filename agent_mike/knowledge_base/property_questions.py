from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from google.adk.tools import ToolContext
from typing import Optional

load_dotenv()
kb_path = os.getenv("PROPERTY_INFO")
print(f"KB PATH BEFORE MODIFICATION: {kb_path}")
kb_path = kb_path.replace("\\", "/")
print(f"KB PATH AFTER MODIFICATION: {kb_path}")
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))


def load_document(file_path):
    """Load Document based on the file path"""
    file_extension = os.path.splitext(file_path)[1]

    if file_extension.lower() == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension.lower() == ".txt":
        loader = TextLoader(file_path)
    elif file_extension.lower() in [".docx", "doc"]:
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported File Format")

    return loader.load()


def create_vector_db_from_document(file_path):
    # Load the File
    document = load_document(file_path)

    text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_spliter.split_documents(document)

    db = FAISS.from_documents(docs, embeddings)
    return db


def answer_questions_about_property(
    query: str, tool_context: ToolContext, k: Optional[int] = None
) -> dict:
    """
    Answers questions about a specific property by retrieving relevant info from the knowledge base.
    The query must include the property address for accurate results.

    Args:
        query (str): The user's question, which must contain the property's address.
        k (int, optional): Number of top matching documents to retrieve which depends the amount Info you need. Defaults to 4.

    Returns:
        str: Combined content from the top-k relevant documents.
    """
    if not k or k <= 0:
        k = 4

    try:
        database = create_vector_db_from_document(kb_path)
        docs = database.similarity_search(query=query, k=k)
        docs_page = "".join([d.page_content for d in docs])
        return {"status": "success", "information": docs_page}
    except Exception as e:
        print(f"ERROR: {e}")
        return {
            "status": "failure",
            "message": "There was an error trying to retrieve the information, please try again.",
        }
