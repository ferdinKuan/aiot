from snownlp import SnowNLP

# 自訂關鍵詞與情緒類型對應
mood_keywords = {
    "疲累": ["耍廢", "壓力", "累", "不想動", "無力", "煩躁", "沒精神", "筋疲力盡"],
    "開心": ["開心", "開趴", "開懷", "爽", "快樂", "幸福", "嗨", "放鬆"],
    "傷心": ["難過", "心痛", "崩潰", "哭", "痛苦", "孤單", "悲傷", "委屈"],
    "普通": ["還好", "一般", "沒事", "普普通通", "就那樣", "無聊"]
}

def analyze_mood(text):
    s = SnowNLP(text)

    matched_moods = []
    keywords = s.keywords(limit=5)

    # 用斷詞去找匹配情緒關鍵字
    for word in s.words:
        for mood, kw_list in mood_keywords.items():
            if word in kw_list:
                matched_moods.append(mood)

    # 判斷最常出現的情緒
    if matched_moods:
        mood = max(set(matched_moods), key=matched_moods.count)
    else:
        # 使用 SnowNLP 作為 fallback
        score = s.sentiments
        if score >= 0.6:
            mood = "開心"
        elif score <= 0.4:
            mood = "疲累"
        else:
            mood = "普通"

    return {
        "mood": mood,
        "keywords": keywords
    }
