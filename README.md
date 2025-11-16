# 📘 GuruInsight AI – YouTube Video Keyword Insight Extractor (AI Project)

🚀 GuruInsight AI is an intelligent tool that analyzes any YouTube video, extracts the transcript, identifies where a specific keyword/person/topic is mentioned, and generates a clean, concise summary using Transformer-based NLP models (T5/BART).

This solves a real problem:
👉 Watching long podcasts (1–2 hours)
👉 Searching if someone was mentioned
👉 Understanding what exactly was said
👉 Getting this summary instantly

# 🔥 Features

🎬 Fetch YouTube video transcripts (TimedText + VTT subtitles)
⚡ Whisper fallback for videos without transcripts
🔍 Keyword detection in transcript
🧩 Context extraction around keyword mentions
✨ Transformer-based summarization (Flan-T5)
🌐 Clean Flask Web App UI
⚡ Fast processing using optimized TimedText + VTT scraping
📌 Works for ALL YouTube videos (podcasts, interviews, news, speeches)

# 🧠 How It Works

User enters YouTube URL + keyword
System fetches transcript using:
VTT subtitles (fastest)
TimedText XML
YouTube API
Whisper fallback
Keyword search and segment extraction
Cleaned text passed to Transformer summarizer
Summary displayed on UI


# 🔧 Tech Stack

Python
Flask
NLP & Transformers (Flan-T5 / BART)
YouTube TimedText Parser
Whisper ASR
HTML + CSS

# ▶️ Run the Project Locally
1. Create virtual environment (Python 3.10 recommended)
   python -m venv venv
   venv\Scripts\activate

2. Install dependencies
   pip install -r requirements.txt

3. Start the server
   cd src
   python server.py

4. Open browser
   http://127.0.0.1:5000

# 🎯 Usage Example
Enter:
YouTube URL: https://youtube.com/...
Keyword: Narendra Modi

Output:

Keyword Found: Yes/No
Mentions: X times
Summary: “The speaker mentioned Modi in context of…”

# 📌 Future Enhancements

Multi-keyword batch analysis
Support for Hindi/Marathi subtitles
Speaker diarization (who said what?)
Deploy on Render / Railway
Add JWT authentication

# 👨‍💻 Author

Guru Dahiphale
AI Engineer | Data Science | NLP | Deep Learning
