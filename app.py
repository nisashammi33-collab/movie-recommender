import pickle
import streamlit as st
import requests
import pandas as pd
import os

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- GLOBAL CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #090b10;
    --surface:   #111520;
    --elevated:  #181e2e;
    --accent:    #e8a020;
    --accent2:   #c0392b;
    --text:      #eef0f6;
    --muted:     #7a849a;
    --border:    rgba(255,255,255,0.06);
    --glow:      rgba(232,160,32,0.18);
    --radius:    14px;
}

/* ── App shell ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(232,160,32,0.08) 0%, transparent 65%),
        radial-gradient(ellipse 60% 40% at 100% 100%, rgba(192,57,43,0.07) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--elevated) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--glow) !important;
}
/* The visible selected value text */
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: transparent !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    font-weight: 400 !important;
    min-height: 48px !important;
}
/* Dropdown list */
[data-baseweb="popover"] [role="listbox"] {
    background: var(--elevated) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius) !important;
}
[data-baseweb="popover"] [role="option"] {
    background: var(--elevated) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background: rgba(232,160,32,0.12) !important;
    color: var(--accent) !important;
}

/* ── Primary button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent2) 0%, var(--accent) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    letter-spacing: 0.5px !important;
    padding: 12px 40px !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, filter 0.15s !important;
    box-shadow: 0 4px 20px rgba(232,160,32,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(232,160,32,0.4) !important;
    filter: brightness(1.08) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Movie card ── */
.card-wrap {
    animation: fadeUp 0.45s ease both;
}
.card-wrap:nth-child(1) { animation-delay: 0.05s; }
.card-wrap:nth-child(2) { animation-delay: 0.12s; }
.card-wrap:nth-child(3) { animation-delay: 0.19s; }
.card-wrap:nth-child(4) { animation-delay: 0.26s; }
.card-wrap:nth-child(5) { animation-delay: 0.33s; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}

.movie-card {
    position: relative;
    background: var(--elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: transform 0.22s cubic-bezier(.25,.8,.25,1),
                box-shadow 0.22s,
                border-color 0.22s;
    cursor: default;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-6px) scale(1.015);
    box-shadow: 0 16px 48px rgba(0,0,0,0.55), 0 0 0 1px rgba(232,160,32,0.35);
    border-color: rgba(232,160,32,0.4);
}
.movie-card:hover .card-glow {
    opacity: 1;
}

.card-glow {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, var(--glow), transparent);
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}

.card-body {
    padding: 22px 20px 24px;
}

.card-rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 11px;
    letter-spacing: 2px;
    color: var(--accent);
    margin-bottom: 4px;
}

.card-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 15px;
    line-height: 1.3;
    color: var(--text);
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-badge {
    display: inline-block;
    margin-top: 10px;
    background: rgba(232,160,32,0.12);
    border: 1px solid rgba(232,160,32,0.3);
    border-radius: 50px;
    font-size: 11px;
    color: var(--accent);
    padding: 3px 10px;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* ── Section heading ── */
.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 16px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* ── Hero title ── */
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(90px, 14vw, 160px);
    line-height: 0.92;
    letter-spacing: 4px;
    color: var(--text);
    margin: 0;
}
.hero-title span { color: var(--accent); }

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 20px;
    color: var(--muted);
    font-weight: 300;
    margin-top: 14px;
    letter-spacing: 0.2px;
}

/* ── Result heading ── */
.result-heading {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 36px;
    letter-spacing: 2px;
    color: var(--text);
    margin: 36px 0 24px;
}
.result-heading em {
    color: var(--accent);
    font-style: normal;
}

/* ── Sidebar styles ── */
.sb-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--accent);
    margin-bottom: 8px;
}
.sb-tip {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.6;
}
.sb-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 20px 0;
}

/* ── No-result state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--muted);
    font-size: 15px;
}
.empty-state .icon { font-size: 48px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)


# -------------------- LOAD MODELS --------------------
@st.cache_resource
def load_models():
    try:
        base_dir = os.path.dirname(__file__)
        movies_path = os.path.join(base_dir, 'movie_list.pkl')
        similarity_path = os.path.join(base_dir, 'similarity.pkl')

        with open(movies_path, 'rb') as f:
            movies = pickle.load(f)
        with open(similarity_path, 'rb') as f:
            similarity = pickle.load(f)

        return movies, similarity

    except Exception as e:
        st.error(f"❌ Error loading model files: {e}")
        return None, None


movies, similarity = load_models()


# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )

        recommended_movies = []

        for i in movies_list[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)

        return recommended_movies

    except Exception as e:
        st.error(f"❌ Recommendation error: {e}")
        return []


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown('<div class="sb-label">🎬 CineMatch</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sb-tip">Discover movies that match your taste using content-based filtering.</p>',
        unsafe_allow_html=True
    )
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sb-label">📖 How it works</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sb-tip">1. Pick a movie you love<br>2. Hit <b>Find Similar</b><br>3. Get 5 hand-picked recommendations</p>',
        unsafe_allow_html=True
    )
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

    if movies is not None:
        total = len(movies)
        st.markdown('<div class="sb-label">📊 Library</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="sb-tip">{total:,} movies indexed</p>', unsafe_allow_html=True)

    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">⚙️ Algorithm</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sb-tip">Content-based similarity on genres, cast, crew, keywords & overview.</p>',
        unsafe_allow_html=True
    )


# -------------------- MAIN CONTENT --------------------
if movies is None:
    st.stop()

# ── Hero ──────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 32px;">
    <p class="hero-title">CINE<span>MATCH</span></p>
    <p class="hero-sub">Find your next favourite film in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr style="margin-bottom:28px;">', unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────
col_select, col_btn, col_spacer = st.columns([4, 1.4, 2], gap="medium")

with col_select:
    st.markdown('<div class="section-label">CHOOSE A MOVIE</div>', unsafe_allow_html=True)
    selected_movie = st.selectbox(
        label="movie_select",
        options=movies['title'].values,
        label_visibility="collapsed"
    )

with col_btn:
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
    do_recommend = st.button("✦ Find Similar", use_container_width=True)

# ── Recommendations ───────────────────────────────────
if do_recommend:
    with st.spinner("Scanning the cinematic universe…"):
        names = recommend(selected_movie)

    if names:
        st.markdown(
            f'<div class="result-heading">Because you like <em>{selected_movie}</em></div>',
            unsafe_allow_html=True
        )

        cols = st.columns(5, gap="medium")

        for idx, (col, name) in enumerate(zip(cols, names)):
            with col:
                st.markdown(f"""
                <div class="card-wrap">
                    <div class="movie-card">
                        <div class="card-glow"></div>
                        <div class="card-body">
                            <div class="card-rank">#{idx+1} PICK</div>
                            <p class="card-title">{name}</p>
                            <span class="card-badge">&#10022; Recommended</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🎭</div>
            <p>No recommendations found for this title.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Idle prompt
    st.markdown("""
    <div class="empty-state" style="padding:80px 20px;">
        <div class="icon">🍿</div>
        <p>Select a movie above and hit <b>Find Similar</b> to get started.</p>
    </div>
    """, unsafe_allow_html=True)
