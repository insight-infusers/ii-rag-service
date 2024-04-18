from transformers import AutoTokenizer, AutoModel

class EmbeddingEngine:
    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed_text(self, text: str) -> List[float]:
        # Tokenize and encode the text for the model
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        # Extract embeddings, for example, mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().tolist()[0]
        return embeddings
