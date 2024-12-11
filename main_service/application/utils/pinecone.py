from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

class PineconeService:
    def __init__(self, index_name: str):
        """
        Initialize Pinecone client and connect to the specified index.
        """
        api_key = os.getenv("PINECONE_API_KEY")
        pc=Pinecone(api_key=api_key)
        self.index_name = index_name
        self.index = pc.Index(index_name)

    def upsert(self, id: str, vector: List[float], metadata: dict = {}):
        """
        Upsert a single vector to Pinecone.
        """
        self.index.upsert(vectors=[{"id": id, "values": vector, "metadata": metadata}])

    def query(self, query_vector: List[float], top_k: int = 1, filter: dict = None):
        """
        Query the Pinecone index with a vector.
        """
        return self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_values=False,
            include_metadata=False,
            filter=filter
        )