from typing import Type, List
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class LLMClient:
    def __init__(self, base_url: str, model: str, provider: str):
        """
        Initializes the LLM client with the API configuration.

        :param base_url: The base URL of the LLM API.
        :param api_key: The API key for authentication.
        :param model: The name of the LLM model to use.
        """
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            client = OpenAI(
                    api_key=api_key,
                )
        else:
            api_key = "ollama"
            client = OpenAI(
                    api_key=api_key,
                    base_url=base_url,
                )
        self.client = client
        self.model = model

    def call_model(self, system_message: str, user_message: str, response_model: Type[BaseModel]):
        """
        Calls the LLM with the provided system message, user message, and response model.

        :param system_message: The system message defining the task for the LLM.
        :param user_message: The user-provided input for the task.
        :param response_model: The Pydantic model to validate the response.
        :return: Parsed response as an instance of the response_model, or None if there's an error.
        """
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                response_format=response_model,
            )
            return response.choices[0].message.parsed
        except Exception as e:
            print(f"Error calling the model: {e}")
            return None
        
class EmbeddingClient:
    def __init__(self, model: str = "text-embedding-ada-002"):
        """
        Initialize the EmbeddingClient with OpenAI API key and embedding model.
        
        :param api_key: OpenAI API key for authentication.
        :param model: Embedding model to use (default is 'text-embedding-ada-002').
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for a single piece of text.

        :param text: The input text to generate an embedding for.
        :return: A list of floats representing the embedding.
        """
        try:
            client = OpenAI(api_key=self.api_key)
            response = client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return []