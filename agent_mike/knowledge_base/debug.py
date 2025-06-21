from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from google.adk.tools import ToolContext

load_dotenv()
kb_path = os.getenv("COMPANY_INFO")
print(f"KB PATH BEFORE MODIFICATION: {kb_path}")
kb_path = kb_path.replace("\\", "/")
print(f"KB PATH AFTER MODIFICATION: {kb_path}")
