from flask import Flask, request, jsonify, render_template
from mood_utils import analyze_mood
from db_utils import search_restaurants  # 或 search_restaurants_by_mood if you have it

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

    # 查詢推薦餐廳
    recommendations = search_restaurants(mood, user_lat, user_lng)

    return jsonify({
        "mood": mood,
        "keywords": keywords,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
