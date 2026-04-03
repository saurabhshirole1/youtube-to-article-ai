"""
article_generator.py
─────────────────────
Calls Groq API (LLaMA-3) to convert a raw YouTube transcript
into a well-structured, readable article.

Returns: (article_text, error_message)
"""

import os
from groq import Groq


# Map UI labels to approximate word counts
LENGTH_MAP = {
    "Short (~300 words)": 300,
    "Medium (~600 words)": 600,
    "Long (~1000 words)": 1000,
}

# Map UI labels to tone instructions
STYLE_MAP = {
    "Informative Blog": (
        "an engaging, informative blog post with a warm, conversational tone. "
        "Include key insights, real-world implications, and takeaways."
    ),
    "Technical Deep-Dive": (
        "a detailed technical article. Use precise terminology, explain concepts "
        "thoroughly, and include technical context and reasoning."
    ),
    "Beginner-Friendly": (
        "a beginner-friendly article that explains every concept simply. "
        "Avoid jargon, use analogies, and keep sentences short."
    ),
    "News Summary": (
        "a concise news-style summary. Lead with the most important point, "
        "follow the inverted pyramid structure, and remain objective."
    ),
}


def build_prompt(transcript: str, title: str, style: str, length: str) -> str:
    word_count = LENGTH_MAP.get(length, 600)
    style_desc = STYLE_MAP.get(style, STYLE_MAP["Informative Blog"])

    # Trim transcript to avoid token limit issues (~12,000 chars ≈ safe for LLaMA-3)
    max_chars = 12_000
    trimmed = transcript[:max_chars]
    if len(transcript) > max_chars:
        trimmed += "\n\n[Transcript trimmed for length]"

    prompt = f"""You are an expert content writer. Your task is to transform a YouTube video transcript into a polished article.

VIDEO TITLE: {title}

ARTICLE REQUIREMENTS:
- Style: Write as {style_desc}
- Target length: approximately {word_count} words
- Structure: Use a compelling title, introduction, 2–4 body sections with clear headings (##), and a conclusion
- Do NOT mention "transcript" or "video" — write as if it's an original article
- Do NOT add any preamble like "Here is your article" — start directly with the title

TRANSCRIPT:
{trimmed}

Now write the article:"""
    return prompt


def generate_article(
    transcript: str,
    video_title: str,
    article_style: str,
    article_length: str,
) -> tuple[str, str | None]:
    """
    Main function called by app.py.

    Returns
    -------
    article_text : str        – Generated article
    error        : str | None – Error message, or None on success
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "", "GROQ_API_KEY not set."

    try:
        client = Groq(api_key=api_key)
        prompt = build_prompt(transcript, video_title, article_style, article_length)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048,
        )

        article = response.choices[0].message.content.strip()
        return article, None

    except Exception as e:
        return "", f"Groq API error: {e}"
