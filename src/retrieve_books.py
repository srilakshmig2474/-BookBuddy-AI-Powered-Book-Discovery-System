
import faiss
import pickle
import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer
BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DIR = BASE_DIR / "vectorstore"
print("Loading FAISS database...")
index = faiss.read_index(
    str(VECTOR_DIR / "books.index")
)
with open(VECTOR_DIR / "book_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
def retrieve_books(query, top_k=5):
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")
    scores, indices = index.search(
        query_embedding, top_k
    )
    print("\nUser query:", query)
    print("\nRecommended books:\n")
    for rank, (score, idx) in enumerate(
        zip(scores[0], indices[0]), start=1
    ):
        book = metadata[idx]
        print(f"\n{rank}. {book['title']}")
        print("Author:", book['author'])
        print("Genre:", book['genres'])
        print("Rating:", book['rating'])
        print("Similarity score:", round(float(score), 4))
        print("Description:", book['description'][:250])
if __name__ == "__main__":

    user_query = input(
        "\nWhat kind of books do you want to read? "
    )

    retrieve_books(user_query, top_k=5)
