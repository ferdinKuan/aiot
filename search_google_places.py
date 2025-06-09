import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

mood_to_keywords = {
    "開心": ["火鍋", "壽司"],
    "傷心": ["咖啡廳", "甜點"],
    "疲累": ["早午餐", "便當"],
    "普通": ["小吃", "早餐"]
}

intent_keywords = {
    "聊天": ["聊天", "聊聊", "朋友", "聚會"],
    "獨處": ["一個人", "安靜", "靜靜", "放空"],
    "大吃": ["大吃", "吃到飽", "慶祝", "狂吃"],
    "療癒": ["療癒", "補充", "壓力", "痛苦", "悲傷"]
}

recommend_by_mood_and_intent = {
    ("開心", "大吃"): ["火鍋", "吃到飽"],
    ("傷心", "獨處"): ["咖啡廳", "甜點"],
    ("疲累", "療癒"): ["早午餐", "蛋糕"],
    ("普通", "聊天"): ["簡餐", "咖啡廳"],
    ("開心", "聊天"): ["居酒屋", "輕食"]
}

def extract_intent(text):
    for intent, words in intent_keywords.items():
        if any(w in text for w in words):
            return intent
    return None

def extract_food_mention(text):
    all_foods = ["壽司", "火鍋", "咖啡廳", "便當", "蛋糕", "甜點", "早午餐", "居酒屋", "吃到飽", "簡餐"]
    return [f for f in all_foods if f in text]

def get_keywords(mood, intent, mentioned_foods):
    if mentioned_foods:
        return mentioned_foods
    if (mood, intent) in recommend_by_mood_and_intent:
        return recommend_by_mood_and_intent[(mood, intent)]
    return mood_to_keywords.get(mood, ["餐廳"])

def search_places_by_mood(text, mood, lat, lng, radius=1500):
    intent = extract_intent(text)
    mentioned = extract_food_mention(text)
    keywords = get_keywords(mood, intent, mentioned)

    results = []
    for kw in keywords:
        url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            f"location={lat},{lng}&radius={radius}&keyword={kw}&key={API_KEY}"
        )
        resp = requests.get(url).json()
        if "results" in resp:
            for place in resp["results"][:3]:
                results.append({
                    "name": place["name"],
                    "type": kw,
                    "price_level": "$" * place.get("price_level", 2),
                    "latitude": place["geometry"]["location"]["lat"],
                    "longitude": place["geometry"]["location"]["lng"],
                    "mood_tags": mood
                })
    return results