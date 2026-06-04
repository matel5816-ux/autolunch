"""
使用 Overpass API 抓取行天宮附近的餐廳
"""
import sys
import os
import json
import requests
from typing import List, Dict
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.queries import init_db, add_restaurant
from src.models.restaurant import PaymentMethod

# 行天宮座標
COMPANY_LAT = 25.0638409
COMPANY_LON = 121.5334954
SEARCH_RADIUS = 1500  # 公尺

def fetch_restaurants_from_overpass() -> List[Dict]:
    """
    使用 Overpass API 抓取餐廳
    """
    # Overpass API 查詢
    overpass_url = "https://overpass-api.de/api/interpreter"

    # 計算 bbox (south, west, north, east)
    south = COMPANY_LAT - 0.015
    west = COMPANY_LON - 0.015
    north = COMPANY_LAT + 0.015
    east = COMPANY_LON + 0.015

    # 查詢多種餐飲類型
    queries = [
        # 餐廳
        f"""[out:json];
        (
          node["amenity"="restaurant"]({south},{west},{north},{east});
          way["amenity"="restaurant"]({south},{west},{north},{east});
        );
        out center;
        """,
        # 便當店
        f"""[out:json];
        (
          node["shop"="convenience"]({south},{west},{north},{east});
          way["shop"="convenience"]({south},{west},{north},{east});
        );
        out center;
        """,
        # 快餐
        f"""[out:json];
        (
          node["amenity"="fast_food"]({south},{west},{north},{east});
          way["amenity"="fast_food"]({south},{west},{north},{east});
        );
        out center;
        """,
        # 咖啡廳
        f"""[out:json];
        (
          node["amenity"="cafe"]({south},{west},{north},{east});
          way["amenity"="cafe"]({south},{west},{north},{east});
        );
        out center;
        """,
    ]

    all_restaurants = []
    headers = {'User-Agent': 'AutoLunch-Bot/1.0'}

    for i, query in enumerate(queries):
        print(f"\n⏳ 查詢類型 {i+1}/4...")
        try:
            response = requests.post(overpass_url, data=query, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                elements = data.get('elements', [])
                print(f"  ✅ 找到 {len(elements)} 家")
                all_restaurants.extend(elements)
                time.sleep(2)  # 禮貌延遲
            else:
                print(f"  ❌ 查詢失敗: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 錯誤: {e}")

    return all_restaurants

def parse_restaurants(elements: List[Dict]) -> List[Dict]:
    """
    解析 Overpass API 結果
    """
    restaurants = []
    seen = set()

    for elem in elements:
        if elem.get('type') != 'node':
            continue

        tags = elem.get('tags', {})
        name = tags.get('name', '').strip()

        if not name or name in seen:
            continue

        seen.add(name)

        lat = elem.get('lat')
        lon = elem.get('lon')

        if not lat or not lon:
            continue

        # 計算距離
        import math
        lat_diff = lat - COMPANY_LAT
        lon_diff = lon - COMPANY_LON
        distance = math.sqrt(lat_diff**2 + lon_diff**2) * 111000  # 轉換為公尺

        if distance > SEARCH_RADIUS:
            continue

        # 推測價格範圍
        cuisine_type = tags.get('cuisine', '')
        phone = tags.get('phone', '')
        website = tags.get('website', '')

        # 簡單的價格推測邏輯
        if any(x in name for x in ['高檔', '精選', '頂級', '特選']):
            price_range = 'premium'
        elif any(x in name for x in ['便當', '自助', '快餐', '平價']):
            price_range = 'budget'
        else:
            price_range = 'mid'

        # 支付方式（假設都支援現金）
        payment_methods = [PaymentMethod.CASH.value]
        if 'visa' in tags.get('payment:visa', '').lower() or website:
            payment_methods.append(PaymentMethod.LINE_PAY.value)

        restaurant = {
            'name': name,
            'latitude': lat,
            'longitude': lon,
            'cuisine_type': cuisine_type or '未分類',
            'price_range': price_range,
            'payment_methods': json.dumps(payment_methods),
            'address': tags.get('addr:full', '台北市中山區'),
            'phone': phone,
            'rating': 4.0,
            'review_count': 0,
        }

        restaurants.append(restaurant)

    return restaurants

def main():
    """主函數"""
    print("=" * 60)
    print("🍜 行天宮附近餐廳資料抓取")
    print("=" * 60)

    # 初始化資料庫
    print("\n📊 初始化資料庫...")
    init_db()

    # 抓取餐廳
    print("\n🌐 從 Overpass API 抓取餐廳...")
    elements = fetch_restaurants_from_overpass()
    print(f"\n✅ 總共找到 {len(elements)} 筆資料")

    # 解析
    print("\n🔍 解析餐廳資訊...")
    restaurants = parse_restaurants(elements)
    print(f"✅ 解析成功 {len(restaurants)} 家餐廳")

    # 新增到資料庫
    print("\n💾 新增到資料庫...")
    success_count = 0
    for i, restaurant in enumerate(restaurants, 1):
        try:
            add_restaurant(**restaurant)
            success_count += 1
            if i % 10 == 0:
                print(f"  ✅ [{i}/{len(restaurants)}]")
        except Exception as e:
            pass  # 忽略重複或其他錯誤

    print(f"\n✅ 成功新增 {success_count} 家餐廳！")
    print("=" * 60)

if __name__ == '__main__':
    main()
