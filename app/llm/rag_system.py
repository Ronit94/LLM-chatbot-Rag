# from langchain import PromptTemplate
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import Pinecone
# from sentence_transformers import SentenceTransformer
# from langchain.embeddings import HuggingFaceEmbeddings
from config import index_name, pin_cone_api_key
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document

# from app.pincone_init import pc
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
# Pinecone credentials



# Connect to Pinecone
def pdfLoader(file_path) -> str:
    reader = PyPDFLoader(file_path)
    raw_text = ""
    for page in reader.load_and_split():
        raw_text += page.page_content + "\n"
    return raw_text 


def text_spliter(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = CharacterTextSplitter( separator="\n",
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
        )
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    return docs

def load_data_embedding(docs):
    # index = pc.Index(host="INDEX_HOST")
    # Pinecone.from_documents(documents=docs, embedding=embedding_model, index_name=index_name, namespace="default")
    return "Data loaded and embedded successfully."


async def load_llm_model():
    # model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    # embedding_model = HuggingFaceEmbeddings(model=model)
    # if not embedding_model:
    #     raise ValueError("Embedding model could not be initialized. Check your environment variables.")
    return "hello"


def question_answering(query, docs):
    """
    Function to perform question answering using the provided query and documents.
    This is a placeholder function and should be replaced with actual logic.
    """
    # Here you would typically use a model to answer the question based on the documents
    # For now, we will just return a dummy response
    return f"Answer to '{query}' based on provided documents."