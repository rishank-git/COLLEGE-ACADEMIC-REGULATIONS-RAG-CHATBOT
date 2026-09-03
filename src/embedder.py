from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL


class Embedder:
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        print("Embedding model loaded.")

    def encode(self, texts):
        """
        Encode one string or a list of strings.
        Returns embeddings as Python lists.
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings.tolist()