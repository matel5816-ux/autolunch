"""
餐廳資料模型
"""
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class PriceRange(Enum):
    """價格範圍"""
    ECONOMY = 'economy'        # 經濟（50-100元）
    CHEAP = 'cheap'           # 平價（100-150元）
    MID = 'mid'               # 中等（150-250元）
    MID_HIGH = 'mid_high'     # 中高（250-400元）
    PREMIUM = 'premium'       # 高檔（400元以上）


PRICE_RANGE_INFO = {
    'economy': {'name': '經濟', 'min': 50, 'max': 100, 'emoji': '💵'},
    'cheap': {'name': '平價', 'min': 100, 'max': 150, 'emoji': '💵💵'},
    'mid': {'name': '中等', 'min': 150, 'max': 250, 'emoji': '💵💵💵'},
    'mid_high': {'name': '中高', 'min': 250, 'max': 400, 'emoji': '💵💵💵💵'},
    'premium': {'name': '高檔', 'min': 400, 'max': 9999, 'emoji': '💵💵💵💵💵'},
}


class PaymentMethod(Enum):
    """支付方式"""
    LINE_PAY = 'LINE Pay'
    STREET_CASH = '街口支付'
    APPLE_PAY = 'Apple Pay'
    GOOGLE_PAY = 'Google Pay'
    CASH = '現金'


@dataclass
class Restaurant:
    """餐廳資訊"""
    id: int
    name: str
    latitude: float
    longitude: float
    price_range: PriceRange
    cuisine_type: Optional[str] = None
    payment_methods: List[PaymentMethod] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    google_maps_url: Optional[str] = None
    rating: float = 0.0
    review_count: int = 0
    is_active: bool = True
    distance: Optional[float] = None  # 運行時計算，單位：公尺

    def __post_init__(self):
        if self.payment_methods is None:
            self.payment_methods = []

    def has_mobile_payment(self) -> bool:
        """是否支援行動支付"""
        mobile_methods = {PaymentMethod.LINE_PAY, PaymentMethod.STREET_CASH,
                         PaymentMethod.APPLE_PAY, PaymentMethod.GOOGLE_PAY}
        return bool(set(self.payment_methods) & mobile_methods)

    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'price_range': self.price_range.value,
            'cuisine_type': self.cuisine_type,
            'payment_methods': [p.value for p in self.payment_methods],
            'address': self.address,
            'phone': self.phone,
            'google_maps_url': self.google_maps_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'is_active': self.is_active,
            'distance': self.distance,
        }
