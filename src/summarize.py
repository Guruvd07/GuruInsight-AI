from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import math


# -------------------------------------------------
# 1. Load T5/BART Summarization Model
# -------------------------------------------------
class Summarizer:
    def __init__(self, model_name="google/flan-t5-base"):
        print(f"Loading summarization model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # -------------------------------------------------
    # 2. Chunk Long Text (because models have token limits)
    # -------------------------------------------------
    def chunk_text(self, text, max_tokens=350):
        words = text.split()
        chunks = []

        # approx token size = word count
        for i in range(0, len(words), max_tokens):
            chunk = " ".join(words[i:i + max_tokens])
            chunks.append(chunk)

        return chunks

    # -------------------------------------------------
    # 3. Summarize Single Chunk
    # -------------------------------------------------
    def summarize_chunk(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True
        )

        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=40,
            temperature=0.7,
            no_repeat_ngram_size=3
        )

        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # -------------------------------------------------
    # 4. Summarize Full Text (with chunking)
    # -------------------------------------------------
    def summarize_text(self, text):
        if len(text.split()) < 120:  # short text
            return self.summarize_chunk(text)

        chunks = self.chunk_text(text)
        summaries = []

        for chunk in chunks:
            try:
                s = self.summarize_chunk(chunk)
                summaries.append(s)
            except Exception as e:
                print("Chunk summarization error:", e)

        # Summarize the combined chunk summaries
        combined = " ".join(summaries)

        final_summary = self.summarize_chunk(
            "Summarize the following points: " + combined
        )

        return final_summary
