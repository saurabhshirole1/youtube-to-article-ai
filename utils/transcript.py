import re
import os
import yt_dlp


def extract_video_id(url: str):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"embed\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        return "", "", "Could not parse a valid YouTube video ID from the URL."

    full_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": False,
        "subtitleslangs": ["en"],
    }

    # Step 1 — Get video title
    video_title = f"YouTube Video ({video_id})"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(full_url, download=False)
            video_title = info.get("title", video_title)
    except Exception:
        pass

    # Step 2 — Get transcript via subtitles
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(full_url, download=False)

            subtitles = info.get("subtitles", {})
            auto_captions = info.get("automatic_captions", {})

            # Prefer manual English subtitles, fallback to auto-generated
            chosen = subtitles.get("en") or auto_captions.get("en")

            if not chosen:
                # Try any available language
                chosen = next(iter(subtitles.values()), None) or \
                         next(iter(auto_captions.values()), None)

            if not chosen:
                return "", video_title, (
                    "No subtitles or captions found for this video. "
                    "Please try a video that has captions enabled (e.g. TED Talks, tutorials)."
                )

            # Get the json3 format URL for easy parsing
            json3_url = next(
                (f["url"] for f in chosen if f.get("ext") == "json3"), None
            )

            if not json3_url:
                # fallback to first available format
                json3_url = chosen[0]["url"]

            # Download and parse the subtitle content
            import urllib.request
            import json

            with urllib.request.urlopen(json3_url) as response:
                content = response.read().decode("utf-8")

            # Try parsing as json3 format
            try:
                data = json.loads(content)
                events = data.get("events", [])
                texts = []
                for event in events:
                    for seg in event.get("segs", []):
                        t = seg.get("utf8", "").strip()
                        if t and t != "\n":
                            texts.append(t)
                transcript_text = " ".join(texts)
            except Exception:
                # Fallback: strip XML/HTML tags if not json
                transcript_text = re.sub(r"<[^>]+>", "", content)
                transcript_text = re.sub(r"&amp;", "&", transcript_text)
                transcript_text = re.sub(r"&lt;", "<", transcript_text)
                transcript_text = re.sub(r"&gt;", ">", transcript_text)

            transcript_text = re.sub(r"\s+", " ", transcript_text).strip()

            if not transcript_text:
                return "", video_title, "Transcript was empty after parsing."

            return transcript_text, video_title, None

    except Exception as e:
        return "", video_title, f"Could not fetch transcript: {e}"