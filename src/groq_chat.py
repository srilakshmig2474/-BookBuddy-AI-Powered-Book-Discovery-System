
import os
import faiss
import pickle
import json

from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq, RateLimitError, AuthenticationError, APIConnectionError

# ----------------------------------
# 1. LOAD CONFIGURATION
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DIR = BASE_DIR / "vectorstore"

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "Groq API key not found. Please check your .env file."
    )

client = Groq(api_key=API_KEY)

# Groq model
GROQ_MODEL = "openai/gpt-oss-20b"


# ----------------------------------
# 2. LOAD FAISS DATABASE
# ----------------------------------

print("Loading FAISS database...")

index = faiss.read_index(
    str(VECTOR_DIR / "books.index")
)

with open(VECTOR_DIR / "book_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

print(f"Total books loaded: {len(metadata)}")


# ----------------------------------
# 3. LOAD EMBEDDING MODEL
# ----------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ----------------------------------
# 4. RETRIEVAL FUNCTION
# ----------------------------------

def retrieve_books(query, top_k=5):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(
        query_embedding, top_k
    )

    retrieved_books = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        book = metadata[idx]

        retrieved_books.append({
            "title": book["title"],
            "author": book["author"],
            "genres": book["genres"],
            "description": book["description"],
            "rating": book["rating"],
            "similarity": float(score)
        })

    return retrieved_books


# ----------------------------------
# 5. GROQ PROMPT ENGINEERING
# ----------------------------------


def generate_recommendations(query, books):

    # Create a unique reference number for each retrieved book.
    book_context = []

    for i, book in enumerate(books, start=1):
        book_context.append({
            "book_id": i,
            "title": book["title"],
            "author": book["author"],
            "genres": str(book["genres"]),
            "description": str(book["description"])[:800]
        })

    prompt = f"""
You are BookBuddy, an English book recommendation assistant.

USER REQUEST:
{query}

AVAILABLE BOOKS:
{json.dumps(book_context, ensure_ascii=False, indent=2)}

TASK:
Select up to 5 books from the AVAILABLE BOOKS that best
match the user's request.

STRICT RULES:

1. Only select books from AVAILABLE BOOKS.

2. Use the exact book_id provided.

3. Never invent or modify a book title or author.

4. Never invent plot details, book characteristics,
   or facts that are not present in the supplied data.

5. Explain why each selected book matches the user's
   request using evidence from its genres and description.

6. Do not claim that a book is beginner-friendly,
   easy to read, short, or suitable for a particular
   age group unless the supplied information supports it.

7. If the user requests a preference that cannot be
   verified from the available data, acknowledge this
   limitation instead of making unsupported claims.

8. If none of the retrieved books are relevant,
   return an empty recommendations list.

9. Recommend only English-language books from
   the supplied list.

OUTPUT:
Return valid JSON only, using this exact structure:

{{
    "recommendations": [
        {{
            "book_id": 1,
            "reason": "A short explanation of why this book matches."
        }}
    ]
}}
"""

    print("Generating recommendations using Groq...")

    try:

        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are BookBuddy. Follow the user's "
                        "instructions strictly and return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_completion_tokens=1200
        )

        response_text = completion.choices[0].message.content

        if not response_text:
            return "Sorry, Groq returned an empty response."

        # Convert Groq's JSON response into a Python dictionary.
        result = json.loads(response_text)

        recommendations = result.get("recommendations", [])

        # Validate each recommendation against the retrieved books.
        verified_recommendations = []
        used_ids = set()

        for item in recommendations:

            book_id = item.get("book_id")

            if not isinstance(book_id, int):
                continue

            if book_id < 1 or book_id > len(books):
                continue

            if book_id in used_ids:
                continue

            original_book = books[book_id - 1]

            reason = str(item.get("reason", "")).strip()

            if not reason:
                continue

            verified_recommendations.append({
                "book": original_book,
                "reason": reason
            })

            used_ids.add(book_id)

        if not verified_recommendations:
            return (
                "I couldn't find sufficiently relevant books "
                "in the retrieved results. Please try another "
                "genre, mood, or reading preference."
            )

        # Return verified recommendation records to Streamlit.
        return verified_recommendations

        for i, recommendation in enumerate(
            verified_recommendations, start=1
        ):

            book = recommendation["book"]
            reason = recommendation["reason"]

            answer += f"""
### {i}. {book['title']}

**Author:** {book['author']}

**Genres:** {book['genres']}

**Rating:** {book['rating']}

**Description:** {book['description']}

**Why it matches:** {reason}

---
"""

        return answer

    except json.JSONDecodeError:

        return (
            "Sorry, I couldn't process the recommendation "
            "response. Please try again."
        )

    except RateLimitError:

        return (
            "BookBuddy has reached the current Groq API usage "
            "limit. Please try again after it resets."
        )

    except AuthenticationError:

        return (
            "Groq authentication failed. Please check your "
            "GROQ_API_KEY in the .env file."
        )

    except APIConnectionError:

        return (
            "Unable to connect to Groq. Please check your "
            "internet connection."
        )

    except Exception as e:

        print("Groq error:", str(e))

        return (
            "Sorry, something went wrong while generating "
            "recommendations."
        )

# ----------------------------------
# 6. MAIN CHAT FUNCTION
# ----------------------------------

def recommend_books(query):

    print("\nSearching for relevant books...")

    books = retrieve_books(query, top_k=5)

    if not books:
        return []

    return generate_recommendations(query, books)


def chat_with_bookbuddy(query):

    recommendations = recommend_books(query)

    if isinstance(recommendations, str):
        return recommendations

    if not recommendations:
        return "Sorry, I couldn't find suitable books."

    answer = "## 📚 BookBuddy Recommendations\n\n"

    for i, item in enumerate(recommendations, start=1):

        book = item["book"]

        answer += f"""
### {i}. {book['title']}

**Author:** {book['author']}

**Genres:** {book['genres']}

**Rating:** {book['rating']}

**Description:** {book['description']}

**Why it matches:** {item['reason']}

---
"""

    return answer

# ----------------------------------
# 7. TEST THE CHATBOT
# ----------------------------------

if __name__ == "__main__":

    print("\n===== BOOKBUDDY CHATBOT =====")
    print("Powered by Groq + FAISS")
    print("Type 'exit' to stop.")

    while True:

        user_query = input("\nYou: ").strip()

        if user_query.lower() == "exit":

            print("Thank you for using BookBuddy!")
            break

        if not user_query:
            continue

        try:

            answer = chat_with_bookbuddy(user_query)

            print("\nBookBuddy:")
            print(answer)

        except Exception as e:

            print("\nError:", str(e))
