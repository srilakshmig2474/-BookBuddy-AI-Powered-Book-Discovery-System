import streamlit as st
import requests

from src.groq_chat import recommend_books


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BookBuddy | Discover your next favourite book",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. CUSTOM DESIGN
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap');

    :root {
        --bb-ink: #20243a;
        --bb-muted: #74788b;
        --bb-purple: #6757d9;
        --bb-purple-dark: #5142bd;
        --bb-paper: #fbf9f5;
        --bb-lavender: #f0edff;
        --bb-border: #e9e5df;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: var(--bb-paper);
        color: var(--bb-ink);
    }

    [data-testid="stHeader"] {
        background: rgba(251, 249, 245, 0.92);
    }

    [data-testid="stSidebar"] {
        background: #f1eff8;
        border-right: 1px solid var(--bb-border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    .brand-mark {
        font-size: 2.7rem;
        line-height: 1;
        text-align: center;
        margin-bottom: 0.35rem;
    }

    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--bb-ink);
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 800;
        letter-spacing: -1.5px;
        text-align: center;
        margin: 0;
    }

    .hero-title span {
        color: var(--bb-purple);
    }

    .hero-subtitle {
        color: var(--bb-muted);
        text-align: center;
        font-size: 1.05rem;
        margin-top: 0.55rem;
    }

    .hero-note {
        text-align: center;
        color: var(--bb-purple-dark);
        background: var(--bb-lavender);
        border: 1px solid #e2dcff;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin: 1.3rem auto 1.5rem auto;
        max-width: 720px;
        font-size: 0.92rem;
    }

    .section-eyebrow {
        color: var(--bb-purple);
        text-transform: uppercase;
        letter-spacing: 1.7px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .section-heading {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--bb-ink);
        font-size: 1.75rem;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 0.25rem;
    }

    .section-description {
        color: var(--bb-muted);
        margin-bottom: 1rem;
        font-size: 0.92rem;
    }

    .sidebar-brand {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.65rem;
        font-weight: 800;
        color: var(--bb-ink);
        margin-bottom: 0;
    }

    .sidebar-copy {
        color: #666b7d;
        font-size: 0.91rem;
        line-height: 1.65;
    }

    .sidebar-label {
        color: var(--bb-ink);
        font-weight: 700;
        font-size: 0.9rem;
        margin: 1.2rem 0 0.5rem 0;
    }

    .genre-pill {
        background: rgba(255,255,255,0.72);
        border: 1px solid #e5e0f1;
        border-radius: 10px;
        padding: 0.55rem 0.7rem;
        margin: 0.38rem 0;
        color: #34384c;
        font-size: 0.88rem;
    }

    .book-card-title {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--bb-ink);
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .book-author {
        color: var(--bb-muted);
        font-size: 0.9rem;
        margin-bottom: 0.7rem;
    }

    .book-label {
        color: var(--bb-purple-dark);
        font-weight: 700;
        font-size: 0.8rem;
        margin-top: 0.7rem;
        margin-bottom: 0.2rem;
    }

    .book-cover-placeholder {
        min-height: 190px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        background: #f0edff;
        border: 1px dashed #d5cef9;
        border-radius: 12px;
        color: #777092;
        text-align: center;
        padding: 0.8rem;
    }

    .book-cover-placeholder span {
        font-size: 2.3rem;
    }

    .stButton > button {
        border-radius: 11px;
        border: 1px solid #e3def5;
        background: #ffffff;
        color: var(--bb-ink);
        font-weight: 600;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        border-color: var(--bb-purple);
        color: var(--bb-purple-dark);
        background: #f8f6ff;
    }

    [data-testid="stChatInput"] {
        border: 1px solid #dcd5f5;
        border-radius: 16px;
        background: #ffffff;
        box-shadow: 0 5px 22px rgba(49, 39, 100, 0.06);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--bb-purple);
        box-shadow: 0 0 0 2px rgba(103, 87, 217, 0.12);
    }

    [data-testid="stChatMessage"] {
        border-radius: 14px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--bb-border);
        border-radius: 16px;
        background: rgba(255,255,255,0.88);
    }

    .footer {
        color: #85889a;
        text-align: center;
        font-size: 0.78rem;
        padding: 1.2rem 0 0.4rem 0;
    }

    @media (max-width: 700px) {
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 0.92rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. BOOK COVER LOOKUP
# =========================================================

@st.cache_data(ttl=86400, show_spinner=False)
def get_book_cover(title, author):
    """Find a likely matching cover in Open Library."""
    def normalize(value):
        return "".join(
            char.lower() for char in str(value) if char.isalnum()
        )

    clean_author = str(author).split("(")[0].strip()
    target_title = normalize(title)
    target_author = normalize(clean_author)

    search_options = [
        {"title": title, "author": clean_author},
        {"title": title},
        {"q": f"{title} {clean_author}"},
    ]

    headers = {"User-Agent": "BookBuddy/1.0 (educational project)"}

    for search_params in search_options:
        try:
            params = {
                **search_params,
                "fields": "title,author_name,cover_i",
                "limit": 10,
            }
            response = requests.get(
                "https://openlibrary.org/search.json",
                params=params,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()

            for result in response.json().get("docs", []):
                cover_id = result.get("cover_i")
                if not cover_id:
                    continue

                result_title = normalize(result.get("title", ""))
                result_authors = result.get("author_name", [])

                title_matches = (
                    result_title == target_title
                    or (
                        len(target_title) >= 8
                        and (
                            target_title in result_title
                            or result_title in target_title
                        )
                    )
                )

                author_matches = any(
                    normalize(name) == target_author
                    or normalize(name) in target_author
                    or target_author in normalize(name)
                    for name in result_authors
                )

                if title_matches and author_matches:
                    return (
                        "https://covers.openlibrary.org/b/id/"
                        f"{cover_id}-M.jpg"
                    )

        except requests.RequestException as error:
            print("Book cover lookup error:", error)

    return None


# =========================================================
# 4. BOOK RECOMMENDATION CARDS
# =========================================================

def display_book_cards(recommendations):
    for number, item in enumerate(recommendations, start=1):
        book = item["book"]
        reason = item.get("reason", "This book matches your interests.")

        with st.container(border=True):
            image_col, details_col = st.columns([1, 3.8], gap="large")

            with image_col:
                cover_url = get_book_cover(
                    book.get("title", ""),
                    book.get("author", ""),
                )

                if cover_url:
                    st.image(cover_url, width=150)
                else:
                    st.markdown(
                        """
                        <div class="book-cover-placeholder">
                            <span>📖</span>
                            <small>Cover not available</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with details_col:
                st.markdown(
                    f'<div class="book-card-title">{number}. '
                    f'{book.get("title", "Untitled")}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="book-author">by '
                    f'{book.get("author", "Unknown author")}</div>',
                    unsafe_allow_html=True,
                )

                genres = book.get("genres")
                if genres:
                    st.markdown(f"**Genre:** {genres}")

                rating = book.get("rating")
                if rating is not None and str(rating).strip():
                    try:
                        rating_value = float(rating)
                        if rating_value > 0:
                            st.markdown(
                                f"⭐ **Dataset rating:** {rating_value:.2f}/5"
                            )
                    except (ValueError, TypeError):
                        pass

                description = book.get("description")
                if description:
                    st.markdown(
                        '<div class="book-label">ABOUT THIS BOOK</div>',
                        unsafe_allow_html=True,
                    )
                    st.write(description)

                st.markdown(
                    '<div class="book-label">WHY IT MATCHES YOUR TASTE</div>',
                    unsafe_allow_html=True,
                )
                st.write(reason)


# =========================================================
# 5. SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# =========================================================
# 6. SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">📚 BookBuddy</div>',
        unsafe_allow_html=True,
    )
    st.caption("YOUR PERSONAL BOOK DISCOVERY SPACE")

    st.markdown("---")

    st.markdown("### About")
    st.markdown(
        """
        <div class="sidebar-copy">
        Discover English books that match your interests, mood,
        favourite themes and reading preferences. Tell BookBuddy
        what you enjoy, and explore your next read.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Explore genres")

    genres = [
        ("✨", "Fantasy & adventure"),
        ("🔍", "Mystery & detective fiction"),
        ("👻", "Horror & thriller"),
        ("🚀", "Science fiction"),
        ("🌱", "Personal growth"),
    ]

    for emoji, genre in genres:
        st.markdown(
            f'<div class="genre-pill">{emoji} &nbsp; {genre}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### How to use")
    st.markdown(
        """
        <div class="sidebar-copy">
        1. Describe the kind of book you want.<br>
        2. BookBuddy searches its book collection.<br>
        3. Explore recommendations selected for you.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if st.button("↻  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()


# =========================================================
# 7. MAIN HERO
# =========================================================

st.markdown(
    """
    <div class="brand-mark">📚</div>
    <h1 class="hero-title">Book<span>Buddy</span></h1>
    <div class="hero-subtitle">
        Find stories that feel like they were chosen just for you.
    </div>
    <div class="hero-note">
        ✨ Your AI-powered guide to discovering English books
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 8. WELCOME AREA AND EXAMPLE PROMPTS
# =========================================================

if not st.session_state.messages:
    st.markdown(
        '<div class="section-eyebrow">A good book is waiting</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-heading">What are you in the mood to read?</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-description">'
        'Choose an idea below or describe your own reading preferences.'
        '</div>',
        unsafe_allow_html=True,
    )

    prompt_columns = st.columns(2, gap="medium")
    example_prompts = [
        "Suggest mystery books with clever detective investigations.",
        "I want fantasy books with magic and adventure.",
        "Recommend emotional romance books with memorable characters.",
        "Suggest beginner-friendly science fiction books.",
    ]

    for index, prompt in enumerate(example_prompts):
        with prompt_columns[index % 2]:
            if st.button(
                prompt,
                key=f"example_prompt_{index}",
                use_container_width=True,
            ):
                st.session_state.pending_query = prompt
                st.rerun()


# =========================================================
# 9. CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        elif message.get("recommendations") is not None:
            st.markdown("### 📚 Your BookBuddy recommendations")
            display_book_cards(message["recommendations"])
        else:
            st.markdown(message.get("content", ""))


# =========================================================
# 10. USER INPUT AND RECOMMENDATIONS
# =========================================================

typed_query = st.chat_input(
    "Describe your ideal book — genre, mood, themes or interests...",
)

user_query = st.session_state.pending_query or typed_query
if st.session_state.pending_query:
    st.session_state.pending_query = None

if user_query:
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Finding books that match your taste..."):
            try:
                recommendations = recommend_books(user_query)

                if isinstance(recommendations, str):
                    st.warning(recommendations)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": recommendations}
                    )

                elif recommendations:
                    st.markdown("### 📚 Your BookBuddy recommendations")
                    display_book_cards(recommendations)
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "recommendations": recommendations,
                        }
                    )

                else:
                    message = (
                        "I couldn't find suitable books for that request. "
                        "Try another genre, theme or reading preference."
                    )
                    st.info(message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": message}
                    )

            except Exception as error:
                st.error(
                    "Something went wrong while finding recommendations. "
                    "Please try again."
                )
                print("Application error:", str(error))


# =========================================================
# 11. FOOTER
# =========================================================

st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <strong>BookBuddy</strong> · AI-powered English Book Discovery<br>
        Built with Python · Streamlit · Sentence Transformers · FAISS · Groq
    </div>
    """,
    unsafe_allow_html=True,
)
