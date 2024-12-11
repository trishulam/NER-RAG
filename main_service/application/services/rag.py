from application.utils.llm_client import EmbeddingClient, LLMClient
from application.utils.pinecone import PineconeService
from application.config import LLAMA_URL
from application.prompts.rag import rag_system_message, rag_user_message
from application.schema.rag import Rag
import os

def generate_embedding(text: str):
    """
    Generate an embedding for a given text.
    """
    embedding_client = EmbeddingClient()
    embedding = embedding_client.get_embedding(text)
    return embedding


def add_document(document_id: str, document_content: str):
    """
    Add a document and its embedding to the VectorDB collection.
    """
    pinecone= PineconeService(index_name=os.getenv("PINECONE_INDEX_NAME"))
    embedding=generate_embedding(document_content)
    pinecone.upsert(id=document_id, vector=embedding)
    return {"message": "Document added successfully"}

def query_documents(query: str,n_results: int = 1):
    """
    Query documents based on embedding similarity.
    """
    pinecone= PineconeService(index_name=os.getenv("PINECONE_INDEX_NAME"))
    embedding=generate_embedding(query)
    results = pinecone.query(query_vector=embedding, top_k=n_results)
    return results

def call_model(query: str,text: str, entities: dict, relationships: dict, provider: str = "openai"):
    """
    Call the LLM model with the provided system message and user message.
    """
    if provider == "openai":
        llm_client = LLMClient(
                base_url="",
                model="gpt-4o-mini",
                provider="openai",
            )
    else:
        llm_client = LLMClient(
            base_url=f"http://{LLAMA_URL}:11434/v1",
            model="llama3.2",
            provider="llama",
        )
    user_message = rag_user_message.format(query=query ,text=text, entities=entities, relationships=relationships)
    response = llm_client.call_model(rag_system_message, user_message, response_model=Rag)
    return response