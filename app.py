import streamlit as st
import os
from dotenv import load_dotenv
from utils.transcript import get_transcript
from utils.article_generator import generate_article
from utils.pdf_generator import generate_pdf

load_dotenv()

# Load from Streamlit Cloud secrets if available
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube → Article & PDF",
    page_icon="🎬",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

h1, h2, h3 { font-family: 'Syne', sans-serif; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.15;
    background: linear-gradient(135deg, #FF6B35, #F7C948, #FF6B35);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.subtitle {
    color: #888;
    font-size: 1rem;
    margin-top: -0.5rem;
    margin-bottom: 1.5rem;
}

.step-badge {
    display: inline-block;
    background: #FF6B35;
    color: white;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.article-box {
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.8rem;
    color: #e0e0e0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    line-height: 1.8;
    white-space: pre-wrap;
}

.stButton > button {
    background: linear-gradient(135deg, #FF6B35, #F7C948);
    color: white;
    border: none;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.6rem 2rem;
    border-radius: 8px;
    transition: opacity 0.2s;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85; }

.info-pill {
    display: inline-block;
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 0.8rem;
    color: #aaa;
    margin: 2px;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎬 YouTube → Article & PDF</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste any YouTube URL. Get a full article + downloadable PDF — powered by Groq AI.</div>', unsafe_allow_html=True)
st.divider()

# # ── API Key ───────────────────────────────────────────────────────────────────
# with st.expander("⚙️ API Configuration", expanded=False):
#     groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...",
#                              help="Get your free key at console.groq.com")
#     if groq_key:
#         os.environ["GROQ_API_KEY"] = groq_key

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<span class="step-badge">Step 1</span>', unsafe_allow_html=True)
youtube_url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed"
)

col1, col2 = st.columns(2)
with col1:
    article_style = st.selectbox("Article Style", ["Informative Blog", "Technical Deep-Dive", "Beginner-Friendly", "News Summary"])
# with col2:
#     article_length = st.selectbox("Article Length", ["Short (~300 words)", "Medium (~600 words)", "Long (~1000 words)"])

# ── Generate Button ───────────────────────────────────────────────────────────
st.markdown("")
generate_btn = st.button("🚀 Generate Article & PDF")

# ── Logic ─────────────────────────────────────────────────────────────────────
if generate_btn:
    if not youtube_url.strip():
        st.error("Please enter a YouTube URL.")
    elif not os.environ.get("GROQ_API_KEY"):
        st.error("Please enter your Groq API key above.")
    else:
        # Step 1 — Transcript
        with st.spinner("📥 Extracting transcript from YouTube..."):
            transcript, video_title, error = get_transcript(youtube_url)

        if error:
            st.error(f"Transcript Error: {error}")
        else:
            st.success(f"✅ Transcript extracted — **{len(transcript.split())} words**")
            st.markdown(f'<span class="info-pill">🎞 {video_title}</span>', unsafe_allow_html=True)

            with st.expander("📄 View Raw Transcript"):
                st.text_area("Transcript", transcript[:3000] + ("..." if len(transcript) > 3000 else ""), height=200)

            # Step 2 — Article
            st.markdown('<span class="step-badge">Step 2</span>', unsafe_allow_html=True)
            with st.spinner("✍️ Generating article with Groq AI..."):
                article, gen_error = generate_article(transcript, video_title, article_style, article_length)

            if gen_error:
                st.error(f"Generation Error: {gen_error}")
            else:
                st.success("✅ Article generated successfully!")
                st.markdown("### 📝 Generated Article")
                st.markdown(f'<div class="article-box">{article}</div>', unsafe_allow_html=True)

                # Step 3 — PDF
                st.markdown('<span class="step-badge">Step 3</span>', unsafe_allow_html=True)
                with st.spinner("📄 Creating PDF..."):
                    pdf_bytes, pdf_error = generate_pdf(article, video_title)

                if pdf_error:
                    st.error(f"PDF Error: {pdf_error}")
                else:
                    st.success("✅ PDF ready!")
                    safe_title = "".join(c for c in video_title if c.isalnum() or c in " _-")[:40]
                    st.download_button(
                        label="⬇️ Download PDF Article",
                        data=pdf_bytes,
                        file_name=f"{safe_title}.pdf",
                        mime="application/pdf",
                    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center><small style='color:#555'>Built with Streamlit · Groq LLaMA · youtube-transcript-api · FPDF2</small></center>",
    unsafe_allow_html=True
)
