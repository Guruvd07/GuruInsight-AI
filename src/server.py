from flask import Flask, request, render_template, jsonify
from app import analyze_video

app = Flask(__name__)


# ----------------------------------------------
# Home Page (UI)
# ----------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------------------------
# API Route for Analysis
# ----------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.form
    url = data.get("url")
    keyword = data.get("keyword")

    if not url or not keyword:
        return jsonify({"error": "URL and keyword are required!"})

    print("Processing:", url, keyword)
    result = analyze_video(url, keyword)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
