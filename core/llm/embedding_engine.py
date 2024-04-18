#from transformers import AutoTokenizer, AutoModel
from typing import List
import asyncio
import openai
from abc import ABC, abstractmethod

class EmbeddingEngine(ABC):
    @abstractmethod
    def __init__(self, model:str):
        pass

    @abstractmethod
    async def get_embedding(self, text: str):
        pass

class BertEmbeddingEngine:
    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    async def embed_text(self, text: str) -> List[float]:
        # Tokenize and encode the text for the model
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        # Extract embeddings, for example, mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().tolist()[0]
        return embeddings


class OpenAIEmbeddingEngine(EmbeddingEngine):
    AVAILABLE_MODELS = {
        'text-embedding-3-large': 3072,
        'text-embedding-3-small': 1536,
        'text-embedding-ada-002': 1536
    }

    def __init__(self, api_key: str, model: str = 'text-embedding-3-small'):
        self.api_key = api_key
        openai.api_key = api_key
        self.client = openai.AsyncOpenAI(api_key=api_key)
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model must be one of {list(self.AVAILABLE_MODELS.keys())}")
        self.model = model

    async def get_embedding(self, text: str):
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            # Add error handling here
            print(f"An error occurred: {e}")
            return None

# Usage example:
async def main(api_key):
    engine = OpenAIEmbeddingEngine(api_key=api_key, model='text-embedding-3-small')
    text = "Transformers are models that process data in a way that is aware of the relationships between all words in a sentence."
    embedding = await engine.get_embedding(text)
    print(embedding)

if __name__ == "__main__":
    import config
    print(config.settings.to_dict())
    asyncio.run(main(config.settings["OPENAI_API_KEY"]))

