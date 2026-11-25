
import re

HOOK_WORDS = [
    "secret", "amazing", "important", "mistake",
    "never", "best", "worst", "why", "how",
    "surprising", "incredible", "actually",
    "problem", "solution", "truth", "finally"
]

def score_segment(text: str) -> int:
    text_lower = text.lower()
    score = 30

    for word in HOOK_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
            score += 5

    if "?" in text:
        score += 10

    if "!" in text:
        score += 5

    if len(text.split()) >= 15:
        score += 10

    return min(score, 100)


def detect_highlights(segments, limit=5):
    highlights = []

    for segment in segments:
        text = segment.get("text", "").strip()

        if not text:
            continue

        highlights.append({
            "start_time": segment["start"],
            "end_time": segment["end"],
            "duration": round(
                segment["end"] - segment["start"], 2
            ),
            "transcript": text,
            "score": score_segment(text)
        })

    highlights.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return highlights[:limit]
