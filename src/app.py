from extract import get_transcript
from search import (
    transcript_to_text,
    find_keyword_segments,
    merge_contexts
)
from summarize import Summarizer


# -------------------------------------------------
# MASTER PIPELINE FUNCTION
# -------------------------------------------------
def analyze_video(url: str, keyword: str):
    """
    Complete pipeline:
    1. Get transcript (YT API → Whisper)
    2. Convert transcript to searchable text
    3. Find keyword segments
    4. Merge context
    5. Summarize using T5
    6. Return final results
    """

    print("\n--- STEP 1: Fetching Transcript ---")
    transcript = get_transcript(url)

    if not transcript:
        return {
            "status": "error",
            "message": "Transcript could not be extracted."
        }

    print("\n--- STEP 2: Preparing Transcript ---")
    full_text, segments = transcript_to_text(transcript)

    print(f"Total transcript length: {len(full_text.split())} words")

    print("\n--- STEP 3: Searching for Keyword ---")
    keyword_segments = find_keyword_segments(segments, keyword, window=2)

    if len(keyword_segments) == 0:
        return {
            "status": "success",
            "keyword_found": False,
            "keyword": keyword,
            "mentions": 0,
            "message": f"Keyword '{keyword}' not found in this video.",
        }

    print(f"Keyword found {len(keyword_segments)} times!")

    print("\n--- STEP 4: Extracting Context ---")
    merged_context_text = merge_contexts(keyword_segments)

    print(f"Context length: {len(merged_context_text.split())} words")

    print("\n--- STEP 5: Summarizing ---")
    summarizer = Summarizer("google/flan-t5-base")
    final_summary = summarizer.summarize_text(
        f"Summarize what the speaker said about {keyword}: " + merged_context_text
    )

    # -------------------------------------------------
    # FINAL RESULT → JSON RESPONSE
    # -------------------------------------------------
    return {
        "status": "success",
        "keyword_found": True,
        "keyword": keyword,
        "mentions": len(keyword_segments),
        "segments": keyword_segments,
        "summary": final_summary
    }


# -------------------------------------------------
# OPTIONAL: Test the pipeline locally
# -------------------------------------------------
if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    keyword = input("Enter keyword to search: ")

    result = analyze_video(url, keyword)
    print("\n\nFINAL OUTPUT:\n", result)
