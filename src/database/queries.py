"""
資料庫查詢函數
"""
import sqlite3
import os
from typing import List, Optional
from src.models.restaurant import Restaurant, PriceRange, PaymentMethod
from src.config import get_config

config = get_config()


def get_db_connection():
    """獲取資料庫連接"""
    db_path = config.DATABASE_URL.replace('sqlite:///', '').replace('sqlite:///:memory:', ':memory:')

    # 確保資料庫目錄存在
    if db_path != ':memory:':
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化資料庫"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            cuisine_type TEXT,
            price_range TEXT NOT NULL,
            payment_methods TEXT,
            address TEXT,
            phone TEXT,
            google_maps_url TEXT,
            rating FLOAT DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            last_verified_date DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 建立索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_price_range ON restaurants(price_range)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_is_active ON restaurants(is_active)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_latitude_longitude ON restaurants(latitude, longitude)')

    conn.commit()
    conn.close()


def add_restaurant(
    name: str,
    latitude: float,
    longitude: float,
    price_range: str,
    cuisine_type: Optional[str] = None,
    payment_methods: Optional[str] = None,
    address: Optional[str] = None,
    phone: Optional[str] = None,
    google_maps_url: Optional[str] = None,
    rating: float = 0,
    review_count: int = 0,
) -> int:
    """
    新增餐廳

    Args:
        name: 餐廳名稱
        latitude: 緯度
        longitude: 經度
        price_range: 價格範圍 (budget/mid/premium)
        cuisine_type: 菜系
        payment_methods: 支付方式 (JSON 格式)
        address: 地址
        phone: 電話
        google_maps_url: Google Maps URL
        rating: 評分
        review_count: 評論數

    Returns:
        新增的餐廳 ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO restaurants (
            name, latitude, longitude, price_range, cuisine_type,
            payment_methods, address, phone, google_maps_url,
            rating, review_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name, latitude, longitude, price_range, cuisine_type,
        payment_methods, address, phone, google_maps_url,
        rating, review_count
    ))

    restaurant_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return restaurant_id


def get_all_restaurants() -> List[Restaurant]:
    """取得所有餐廳"""
    from src.services.geometry_service import GeometryService

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM restaurants WHERE is_active = 1')
    rows = cursor.fetchall()
    conn.close()

    restaurants = []
    for row in rows:
        payment_methods = []
        if row['payment_methods']:
            import json
            payment_methods = [PaymentMethod(m) for m in json.loads(row['payment_methods'])]

        restaurant = Restaurant(
            id=row['id'],
            name=row['name'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            price_range=PriceRange(row['price_range']),
            cuisine_type=row['cuisine_type'],
            payment_methods=payment_methods,
            address=row['address'],
            phone=row['phone'],
            google_maps_url=row['google_maps_url'],
            rating=row['rating'],
            review_count=row['review_count'],
            is_active=bool(row['is_active']),
        )

        # 計算距離
        distance = GeometryService.haversine_distance(
            config.COMPANY_LATITUDE, config.COMPANY_LONGITUDE,
            restaurant.latitude, restaurant.longitude
        )
        restaurant.distance = distance

        restaurants.append(restaurant)

    return restaurants


def get_restaurant_by_id(restaurant_id: int) -> Optional[Restaurant]:
    """根據 ID 取得餐廳"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM restaurants WHERE id = ?', (restaurant_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    payment_methods = []
    if row['payment_methods']:
        import json
        payment_methods = [PaymentMethod(m) for m in json.loads(row['payment_methods'])]

    return Restaurant(
        id=row['id'],
        name=row['name'],
        latitude=row['latitude'],
        longitude=row['longitude'],
        price_range=PriceRange(row['price_range']),
        cuisine_type=row['cuisine_type'],
        payment_methods=payment_methods,
        address=row['address'],
        phone=row['phone'],
        google_maps_url=row['google_maps_url'],
        rating=row['rating'],
        review_count=row['review_count'],
        is_active=bool(row['is_active']),
    )


def delete_restaurant(restaurant_id: int) -> bool:
    """刪除餐廳（軟刪除）"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('UPDATE restaurants SET is_active = 0 WHERE id = ?', (restaurant_id,))
    conn.commit()
    conn.close()

    return cursor.rowcount > 0
