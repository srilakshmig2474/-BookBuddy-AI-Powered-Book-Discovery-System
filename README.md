# 📚 BookBuddy AI – AI-Powered Book Discovery and Recommendation System

BookBuddy AI is an intelligent book discovery and recommendation system that helps users find English books based on their interests and natural-language queries. It combines Semantic Search, Retrieval-Augmented Generation (RAG), and Generative AI to provide relevant and personalized book recommendations.

Users can interact with the application through a simple chat interface and receive book suggestions along with descriptions, ratings, authors, and available cover images.

## 🚀 Features

- **AI-Powered Recommendations:** Generates personalized book suggestions using a Large Language Model.
- **Semantic Search:** Understands the meaning and context of user queries instead of relying only on keywords.
- **RAG-Based Retrieval:** Combines relevant book retrieval with AI-generated responses.
- **Vector Similarity Search:** Uses FAISS to retrieve the top five relevant books.
- **Interactive Interface:** Provides a user-friendly chatbot using Streamlit.
- **Book Details:** Displays titles, authors, genres, descriptions, and ratings.
- **Book Cover Images:** Retrieves available cover images through the Open Library API.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| Pandas | Dataset preprocessing |
| Sentence Transformers | Text embedding generation |
| all-MiniLM-L6-v2 | Embedding model |
| FAISS | Vector similarity search |
| Groq API | LLM integration and recommendation generation |
| openai/gpt-oss-20b | Language model |
| NumPy | Numerical operations |
| Pickle | Book metadata storage |
| Open Library API | Book cover image retrieval |
| python-dotenv | Environment variable management |

## 🏗️ Project Architecture

BookBuddy follows a Retrieval-Augmented Generation (RAG) architecture.

1. **Dataset Preprocessing:** The English book dataset is cleaned and prepared using Pandas.
2. **Embedding Generation:** Sentence Transformers converts book information into numerical vector embeddings.
3. **Vector Database:** FAISS stores the embeddings and enables efficient similarity searching.
4. **Book Retrieval:** User queries are converted into embeddings, and the top five relevant books are retrieved.
5. **AI Recommendation:** Retrieved book information is passed to the Groq API to generate personalized recommendations.
6. **Result Display:** Streamlit displays recommendations, explanations, book details, and available cover images.

## 📂 Project Structure

```text
BookBuddy-AI/
│
├── data/
│   ├── books_train.csv
│   ├── books_test.csv
│   └── english_books.csv
│
├── src/
│   ├── preprocess.py
│   ├── build_vectorstore.py
│   ├── retrieve_books.py
│   └── groq_chat.py
│
├── vectorstore/
│   ├── books.index
│   └── book_metadata.pkl
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/srilakshmig2474/-BookBuddy-AI-Powered-Book-Discovery-System.git
```

### 2. Navigate to the Project Folder

```bash
cd -BookBuddy-AI-Powered-Book-Discovery-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API Key

Create a `.env` file in the project root directory and add:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

**Note:** Never upload your `.env` file or share your API key publicly.

### 6. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 📖 How It Works

1. Open the BookBuddy application.
2. Enter your reading interests or describe the type of book you want.
3. The system searches for relevant books using semantic similarity.
4. The Groq-powered language model generates recommendations based on retrieved books.
5. Explore the recommended books and their available details.

**Example Queries:**

- Suggest fantasy books with magic and adventure.
- Recommend mystery books with detective stories.
- I want science fiction books about space and technology.
- Suggest books with inspiring life lessons.

## 🔮 Future Enhancements

- User registration and authentication.
- Personalized recommendations based on reading history.
- Reading lists and bookmarks.
- Advanced genre and rating filters.
- Multilingual book recommendations.
- User reviews and feedback.
- Expansion of the book dataset.

## 🎯 Project Objective

The main objective of BookBuddy AI is to simplify book discovery by combining semantic search, vector databases, and Generative AI. It demonstrates the practical application of Retrieval-Augmented Generation in building intelligent recommendation systems.

## 👩‍💻 Developed As

**Project:** BookBuddy AI – AI-Powered Book Discovery and Recommendation System

**Internship:** SkillDzire – Generative AI with LLMs

**Domain:** Artificial Intelligence and Generative AI

---

⭐ If you find this project interesting, consider giving the repository a star!
