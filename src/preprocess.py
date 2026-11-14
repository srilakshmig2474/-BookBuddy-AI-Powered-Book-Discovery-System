
import pandas as pd
from pathlib import Path

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Load both CSV files
print("Loading book datasets...")

train_df = pd.read_csv(DATA_DIR / "books_train.csv")
test_df = pd.read_csv(DATA_DIR / "books_test.csv")

print(f"Training records: {len(train_df)}")
print(f"Testing records: {len(test_df)}")

# Combine both datasets
books_df = pd.concat(
    [train_df, test_df],
    ignore_index=True
)

print(f"\nTotal records: {len(books_df)}")

# Select only English books
books_df["language"] = (
    books_df["language"]
    .astype("string")
    .str.strip()
)

english_books = books_df[
    books_df["language"].str.casefold() == "english"
].copy()

print(f"English books: {len(english_books)}")

# Remove records with missing titles or descriptions
english_books["description"] = (
    english_books["description"]
    .fillna("")
    .astype(str)
    .str.strip()
)

english_books["title"] = (
    english_books["title"]
    .fillna("")
    .astype(str)
    .str.strip()
)

english_books["author"] = (
    english_books["author"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

english_books = english_books[
    (english_books["title"] != "") &
    (english_books["description"] != "")
].copy()

# Remove duplicate book IDs
english_books = english_books.drop_duplicates(
    subset=["id"],
    keep="first"
)

# Remove duplicate title-author combinations
english_books = english_books.drop_duplicates(
    subset=["title", "author"],
    keep="first"
)

# Keep only useful columns for recommendations
useful_columns = [
    "id",
    "title",
    "author",
    "genres",
    "description",
    "rating",
    "numRatings",
    "pages",
    "publisher",
    "language"
]

english_books = english_books[useful_columns].copy()

# Create a combined text field for future embeddings
def create_book_text(row):
    return f"""
Title: {row['title']}
Author: {row['author']}
Genres: {row['genres']}
Description: {row['description']}
Rating: {row['rating']}
Pages: {row['pages']}
"""

english_books["book_text"] = english_books.apply(
    create_book_text,
    axis=1
)

# Save the cleaned dataset
output_path = DATA_DIR / "english_books.csv"

english_books.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

# Display final results
print("\n========== PREPROCESSING COMPLETE ==========")
print(f"Final number of books: {len(english_books)}")
print(f"Saved file: {output_path}")

print("\nSample book records:")
print(
    english_books[
        ["title", "author", "genres"]
    ].head(5).to_string(index=False)
)

print("\nMissing values:")
print(english_books.isnull().sum())
