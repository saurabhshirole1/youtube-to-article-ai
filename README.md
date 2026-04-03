# 🎬 YouTube Video → Insightful Article & PDF

> Paste any YouTube URL → Get a full AI-written article + downloadable PDF in seconds.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA--3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 What This Project Does

This tool automates the full pipeline from a YouTube video to a polished article:

1. **Extracts** the transcript from any YouTube video (no API key required for this step)
2. **Generates** a structured, readable article using Groq's LLaMA-3-70B model
3. **Exports** the article as a formatted, downloadable PDF
4. **Deployed** as an interactive Streamlit web app

---

## 🗂 Project Structure

```
yt_to_article/
│
├── app.py                     # Main Streamlit application
│
├── utils/
│   ├── __init__.py
│   ├── transcript.py          # YouTube transcript extraction
│   ├── article_generator.py   # Groq AI article generation
│   └── pdf_generator.py       # PDF creation with FPDF2
│
├── requirements.txt           # All dependencies
└── README.md                  # Project documentation
```

---

## ⚙️ How It Works — Step by Step

### Step 1 — Transcript Extraction (`utils/transcript.py`)
- Parses the YouTube video ID from any URL format
- Uses `youtube-transcript-api` to fetch the transcript (no YouTube API key needed)
- Uses `yt-dlp` to fetch the video title
- Returns clean, joined transcript text

### Step 2 — Article Generation (`utils/article_generator.py`)
- Sends the transcript to Groq's API with a detailed prompt
- Model used: `llama3-70b-8192` (fast + free tier available)
- Supports 4 article styles and 3 length options
- Returns a Markdown-formatted article

### Step 3 — PDF Export (`utils/pdf_generator.py`)
- Parses the Markdown headings and body text
- Uses FPDF2 to build a professionally formatted PDF
- Includes custom header, footer, page numbers, and brand accent color
- Returns raw bytes for Streamlit's download button

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/yt-to-article.git
cd yt-to-article
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Free Groq API Key
- Visit [console.groq.com](https://console.groq.com)
- Sign up and create an API key (free tier is generous)

### 4. Run the App
```bash
streamlit run app.py
```

### 5. Use the App
1. Expand "⚙️ API Configuration" and paste your Groq API key
2. Paste any YouTube URL
3. Choose article style and length
4. Click **🚀 Generate Article & PDF**
5. Download your PDF!

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `groq` | Groq API client (LLaMA-3) |
| `youtube-transcript-api` | Fetch YT transcripts |
| `yt-dlp` | Fetch video title |
| `fpdf2` | Generate PDF |

---

## 🔑 Environment Variable (Optional)

Instead of entering the API key in the UI every time, you can set it as an environment variable:

```bash
export GROQ_API_KEY=gsk_your_key_here
streamlit run app.py
```

---

## 💡 Supported YouTube URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`

---

## ⚠️ Limitations

- Videos with disabled captions will return an error
- Very long videos (3h+) will have transcripts trimmed to ~12,000 characters for the AI
- Auto-generated captions may have minor transcription errors

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Groq — LLaMA-3 70B
- **Transcript**: youtube-transcript-api
- **PDF**: FPDF2
- **Language**: Python 3.10+

---

## 📄 License

MIT License — free to use and modify.

---

*Built as part of an internship project — transforming video content into readable knowledge.*
