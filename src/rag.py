import chromadb

from src.chunker import AcademicChunker
from src.embedder import Embedder
from src.config import CHROMA_PATH


class AcademicRAG:

    def __init__(self):

        self.embedder = Embedder()

        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))

        self.collection = self.client.get_or_create_collection(
            name="academic_regulations"
        )

    def build_database(self):

        print("Extracting chunks...")

        chunker = AcademicChunker()

        chunks = chunker.process()

        print(f"Found {len(chunks)} chunks")

        texts = [c["text"] for c in chunks]

        print("Generating embeddings...")

        embeddings = self.embedder.encode(texts)

        print("Saving to ChromaDB...")

        self.collection.upsert(
            ids=[c["id"] for c in chunks],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {
                    "section_number": c["section_number"],
                    "section_title": c["section_title"],
                    "category": c["category"],
                }
                for c in chunks
            ],
        )

        print("✅ Database created successfully.")

    def search(self, query, top_k=3):

        embedding = self.embedder.encode(query)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        return results


if __name__ == "__main__":

    rag = AcademicRAG()

    rag.build_database()

