import pymysql

def search_restaurants(mood):
    # 根據你的帳號密碼修改這邊
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='0000',
        database='restaurant_recommendation',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM restaurants
                WHERE mood_tags LIKE %s
                LIMIT 3
            """
            cursor.execute(sql, (f"%{mood}%",))
            results = cursor.fetchall()
            return results
    finally:
        conn.close()
