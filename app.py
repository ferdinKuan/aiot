from flask import Flask, request, jsonify, render_template
from mood_utils import analyze_mood
from db_utils import search_restaurants

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.json.get("text")
    
    # AI 情緒分析
    mood_data = analyze_mood(user_input)
    mood = mood_data["mood"]
    keywords = mood_data["keywords"]
    
    # 查詢資料庫
    recommendations = search_restaurants(mood)

    # 回傳所有結果
    return jsonify({
        "mood": mood,
        "keywords": keywords,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
