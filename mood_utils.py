from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# 載入模型（model/ 資料夾）
tokenizer = AutoTokenizer.from_pretrained("model")
model = AutoModelForSequenceClassification.from_pretrained("model")

# 自行根據你訓練的順序設定
label_map = {
    0: "傷心",
    1: "普通",
    2: "生氣",
    3: "疲累",
    4: "開心"
}

def analyze_mood(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    pred = torch.argmax(probs, dim=1).item()
    mood = label_map[pred]

    return {
        "mood": mood,
        "keywords": []  # 可擴充成自動提取關鍵字
    }
