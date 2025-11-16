import re

# -------------------------------------------------
# 1. Clean Transcript Text
# -------------------------------------------------
def clean_text(text: str) -> str:
    """
    Remove extra spaces, newlines, filler chars.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------------------------------
# 2. Convert transcript list → one big searchable text
# -------------------------------------------------
def transcript_to_text(transcript):
    """
    Combine all transcript entries into one clean text.
    Also returns tuple list: (start, text)
    """
    full_text = ""
    segments = []

    for entry in transcript:
        t = clean_text(entry["text"])
        full_text += " " + t
        segments.append((entry["start"], t))

    full_text = clean_text(full_text)
    return full_text, segments


# -------------------------------------------------
# 3. Search keyword in segments
# -------------------------------------------------
def find_keyword_segments(segments, keyword, window=2):
    """
    Search keyword in each segment.
    window = how many lines before/after to include.
    Returns:
    - list of dicts: {start, context_text}
    """
    keyword = keyword.lower()
    results = []

    for i, (start, text) in enumerate(segments):
        if keyword in text.lower():
            # Collect context
            start_idx = max(0, i - window)
            end_idx = min(len(segments), i + window + 1)

            context_text = " ".join([segments[j][1] for j in range(start_idx, end_idx)])
            context_text = clean_text(context_text)

            results.append({
                "start": start,
                "context": context_text
            })

    return results


# -------------------------------------------------
# 4. Combine all extracted context into one text block
# -------------------------------------------------
def merge_contexts(keyword_segments):
    """
    Merge all extracted contexts into one summary text input.
    Remove duplicates.
    """
    seen = set()
    merged = []

    for seg in keyword_segments:
        ctx = seg["context"]
        if ctx not in seen:
            merged.append(ctx)
            seen.add(ctx)

    return " ".join(merged)
