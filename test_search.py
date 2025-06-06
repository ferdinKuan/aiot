from db_utils import search_restaurants

mood = "疲累"
results = search_restaurants(mood)

for r in results:
    print(f"{r['name']}({r['type']},{r['price_level']}) - mood tags: {r['mood_tags']}")
