"""
示範資料初始化腳本
"""
import json
from src.database.queries import init_db, add_restaurant
from src.models.restaurant import PaymentMethod

# 示範餐廳資料
SAMPLE_RESTAURANTS = [
    {
        'name': '丸龜製麵',
        'latitude': 25.0640,
        'longitude': 121.5340,
        'price_range': 'budget',
        'cuisine_type': '日式烏龍麵',
        'payment_methods': json.dumps([PaymentMethod.LINE_PAY.value, PaymentMethod.STREET_CASH.value]),
        'address': '台北市中山區松江路 364 號',
        'phone': '02-2511-1234',
        'rating': 4.5,
        'review_count': 245,
    },
    {
        'name': '麻辣火鍋',
        'latitude': 25.0645,
        'longitude': 121.5350,
        'price_range': 'mid',
        'cuisine_type': '川式火鍋',
        'payment_methods': json.dumps([PaymentMethod.LINE_PAY.value]),
        'address': '台北市中山區南京東路三段 100 號',
        'phone': '02-2531-5678',
        'rating': 4.2,
        'review_count': 156,
    },
    {
        'name': '時尚鐵板燒',
        'latitude': 25.0635,
        'longitude': 121.5345,
        'price_range': 'premium',
        'cuisine_type': '日式鐵板燒',
        'payment_methods': json.dumps([
            PaymentMethod.LINE_PAY.value,
            PaymentMethod.APPLE_PAY.value,
            PaymentMethod.GOOGLE_PAY.value
        ]),
        'address': '台北市中山區長安東路一段 50 號',
        'phone': '02-2507-9999',
        'rating': 4.8,
        'review_count': 389,
    },
    {
        'name': '便當大王',
        'latitude': 25.0630,
        'longitude': 121.5360,
        'price_range': 'budget',
        'cuisine_type': '台灣便當',
        'payment_methods': json.dumps([PaymentMethod.CASH.value, PaymentMethod.STREET_CASH.value]),
        'address': '台北市中山區漢口街 200 號',
        'phone': '02-2523-1111',
        'rating': 4.0,
        'review_count': 89,
    },
    {
        'name': '義大利麵屋',
        'latitude': 25.0650,
        'longitude': 121.5370,
        'price_range': 'mid',
        'cuisine_type': '義式餐廳',
        'payment_methods': json.dumps([
            PaymentMethod.LINE_PAY.value,
            PaymentMethod.STREET_CASH.value,
            PaymentMethod.APPLE_PAY.value
        ]),
        'address': '台北市中山區西康街 88 號',
        'phone': '02-2502-3456',
        'rating': 4.6,
        'review_count': 267,
    },
    {
        'name': '精選牛肉麵',
        'latitude': 25.0625,
        'longitude': 121.5355,
        'price_range': 'budget',
        'cuisine_type': '台灣牛肉麵',
        'payment_methods': json.dumps([PaymentMethod.CASH.value, PaymentMethod.LINE_PAY.value]),
        'address': '台北市中山區松江路 300 號',
        'phone': '02-2514-5678',
        'rating': 4.3,
        'review_count': 178,
    },
    {
        'name': '高檔壽司吧',
        'latitude': 25.0655,
        'longitude': 121.5365,
        'price_range': 'premium',
        'cuisine_type': '日式壽司',
        'payment_methods': json.dumps([
            PaymentMethod.LINE_PAY.value,
            PaymentMethod.APPLE_PAY.value,
            PaymentMethod.GOOGLE_PAY.value
        ]),
        'address': '台北市中山區八德路二段 100 號',
        'phone': '02-2519-8888',
        'rating': 4.9,
        'review_count': 432,
    },
    {
        'name': '港式茶餐廳',
        'latitude': 25.0638,
        'longitude': 121.5348,
        'price_range': 'mid',
        'cuisine_type': '港式餐廳',
        'payment_methods': json.dumps([PaymentMethod.STREET_CASH.value, PaymentMethod.CASH.value]),
        'address': '台北市中山區伊通街 80 號',
        'phone': '02-2505-2222',
        'rating': 4.1,
        'review_count': 123,
    },
]


def populate_restaurants():
    """初始化示範餐廳資料"""
    print("初始化資料庫...")
    init_db()

    print("新增示範餐廳...")
    for i, restaurant in enumerate(SAMPLE_RESTAURANTS, 1):
        try:
            restaurant_id = add_restaurant(**restaurant)
            print(f"  ✅ [{i}/{len(SAMPLE_RESTAURANTS)}] {restaurant['name']} (ID: {restaurant_id})")
        except Exception as e:
            print(f"  ❌ {restaurant['name']}: {str(e)}")

    print(f"\n✅ 成功新增 {len(SAMPLE_RESTAURANTS)} 間示範餐廳！")
    print("\n提示：")
    print("  - 所有餐廳都在公司附近 25.06 北緯, 121.53 東經")
    print("  - 距離範圍約 300-800 公尺")
    print("  - 包含各種價格範圍和支付方式")
    print("  - 現在可以啟動伺服器進行測試了！")
    print("\n啟動伺服器：python src/main.py")


if __name__ == '__main__':
    populate_restaurants()
