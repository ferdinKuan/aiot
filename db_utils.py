import mysql.connector
import math

def haversine(lat1, lng1, lat2, lng2):
    # ➜ 把 Decimal 轉成 float，避免型別錯誤
    lat1 = float(lat1)
    lng1 = float(lng1)
    lat2 = float(lat2)
    lng2 = float(lng2)

    R = 6371  # 地球半徑（km）
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def search_restaurants(mood, user_lat, user_lng):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0000",
        database="restaurant_recommendation"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM restaurants WHERE mood_tags LIKE %s", (f"%{mood}%",))
    rows = cursor.fetchall()

    # 根據距離排序
    for row in rows:
        row["distance"] = haversine(user_lat, user_lng, row["latitude"], row["longitude"])

    rows.sort(key=lambda x: x["distance"])
    return rows[:5]  # 前 5 筆最近的推薦

