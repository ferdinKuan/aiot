from flask import Flask, request, jsonify, render_template
from mood_utils import analyze_mood
from search_google_places import search_places_by_mood  # ✅ 改這行

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text")
    user_lat = data.get("user_lat")
    user_lng = data.get("user_lng")

    # AI 情緒分析
    mood_result = analyze_mood(text)
    mood = mood_result["mood"]
    keywords = mood_result["keywords"]

    # ✅ 使用 Google Places API 查推薦
    recommendations = search_places_by_mood(text, mood, user_lat, user_lng)

    return jsonify({
        "mood": mood,
        "keywords": keywords,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
