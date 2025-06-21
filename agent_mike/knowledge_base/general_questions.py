from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from google.adk.tools import ToolContext
from typing import Optional

load_dotenv()
kb_path = os.getenv("COMPANY_INFO")
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


def answer_questions_about_company(
    query: str, tool_context: ToolContext, k: Optional[int] = None
) -> dict:
    """
    Answers questions about Skyway Realty by retrieving relevant information from the company knowledge base.
    The query should be related to company details like services, leadership, location, or contact information.

    Args:
        query (str): The user's question related to the company (e.g., services offered, office address).
        k (int, optional): Number of top matching documents to retrieve based on relevance. Defaults to 4.

    Returns:
        str: Combined content from the top-k relevant documents.
    """
    if not k or k <= 0:
        k = 4

    try:
        database = create_vector_db_from_document(kb_path)
        docs = database.similarity_search(query=query, k=k)
        docs_page = "".join([d.page_content for d in docs])
        return {"status": "success", "message": docs_page}
    except Exception as e:
        print(f"ERROR:{e}")
        return {
            "status": "failure",
            "message": "There was an error trying to retrieve the information, please try again later.",
        }
