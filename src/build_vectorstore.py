
import pandas as pd
import numpy as np
import faiss
import pickle

from pathlib import Path
from sentence_transformers import SentenceTransformer

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DIR = BASE_DIR / "vectorstore"
VECTOR_DIR.mkdir(exist_ok=True)
print("Loading English book dataset...")
df = pd.read_csv(DATA_DIR / "english_books.csv")
print(f"Total books: {len(df)}")
print("\nLoading Sentence Transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
book_texts = df["book_text"].fillna("").tolist()
print("\nGenerating book embeddings...")
embeddings = model.encode(
    book_texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)
embeddings = np.asarray(embeddings, dtype="float32")
print("Embedding generation completed!")
print("Embedding shape:", embeddings.shape)
print("\nCreating FAISS vector database...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)
faiss.write_index(
    index,
    str(VECTOR_DIR / "books.index")
)
metadata = df.to_dict(orient="records")

with open(VECTOR_DIR / "book_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("\n========== VECTOR DATABASE CREATED ==========")
print("Total indexed books:", index.ntotal)
print("Vector dimensions:", dimension)
print("Saved index:", VECTOR_DIR / "books.index")
print("Saved metadata:", VECTOR_DIR / "book_metadata.pkl")
