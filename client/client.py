import os, dotenv, numpy as np # Standard Python Imports
from openai import OpenAI

from client.config import * # # Configurations

from typing import List

class OpenAPI:
    """
    The universal OpenAI client, allowing users to interface with the OpenAI API.
    """

    def __init__(self: any, chat_model: str = CHAT_MODEL, embedding_model: str = EMBEDDING_MODEL) -> 'OpenAPI':
        """
        Initializes an OpenAPI instance for interfacing with the OpenAI API.

        @return: An OpenAPI instance with fields set as specified.
        """

        dotenv.load_dotenv()
        self.key: str         = os.getenv('OPENAI_KEY')
        self.api: 'OpenAI'    = OpenAI(api_key=self.key)
        self.embed_model: str = embedding_model
        self.chat_model: str  = chat_model

        self.previous: list[str] = []
        self.embed_tokens: int = 0
        self.chat_tokens: int  = 0


    def embedding(self: any, texts: List[str]) -> np.ndarray:
        """
        Returns the vector embedding of the given text.

        @param text: A string representing the text to embed.
        @return: A vector of floats representing the embedding of the text.
        """

        result = self.api.embeddings.create(model=self.embed_model, input=texts)
        self.embed_tokens += result.usage.total_tokens
        return np.array([item.embedding for item in result.data])


    def similarity(self: any, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Returns the cosine similarity between the two given vector embeddings.

        @param vec1: A vector of floats representing the first embedding.
        @param vec2: A vector of floats representing the second embedding.
        @return: A float representing the similarity between the two embeddings.
        """

        num: float = np.dot(vec1, vec2)
        den: float = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        return num / den

    def categorize(self: any, text: str, labels: List[str]) -> str:
        """
        Returns the label of the given text based on the provided labels.

        @param text: A string representing the text to categorize.
        @param labels: A list of strings representing the possible labels.
        @return: A string representing the best label of the text.
        """

        embeddings = self.embedding([text] + labels)
        temb, lemb = embeddings[0], embeddings[1:]
        scores = np.array([self.similarity(temb, label) for label in lemb])
        return labels[np.argmax(scores)], np.max(scores)


    def response(self, message: str, context: str = "", max_tokens: int = 500):
        correction_prompt: str = """You are not allowed to correct the user on 
                                    their message. If you are confused, ask the 
                                    user to clarify or repeat their message."""
        pov_prompt: str = """When you refer to C1C0, always address in first 
                            person because C1C0 is you."""
        total_context = [correction_prompt, pov_prompt] + self.previous + [context]

        try:
            result = self.api.chat.completions.create(
                model=self.chat_model,
                messages=[{"role": "system", "content": " ".join(total_context)}, {"role": "user", "content": message}],
                max_tokens=max_tokens, # Ensures that response is not too long
                stop = [".", "!", "?"] # Ensures that response ends on a complete sentence
            )
            self.chat_tokens += result.usage.total_tokens
            return result.choices[0].message.content

        except Exception as e:
            print(f"API Error with response: {str(e)}")
            return None
