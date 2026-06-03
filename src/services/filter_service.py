"""
餐廳篩選服務 - 根據多個條件篩選
"""
from typing import List
from src.models.restaurant import Restaurant, PriceRange, PaymentMethod
from src.services.geometry_service import GeometryService


class FilterService:
    """餐廳篩選服務"""

    @staticmethod
    def filter_by_price_range(
        restaurants: List[Restaurant], price_ranges: List[PriceRange]
    ) -> List[Restaurant]:
        """
        根據價格範圍篩選

        Args:
            restaurants: 餐廳列表
            price_ranges: 要篩選的價格範圍列表

        Returns:
            篩選後的餐廳列表
        """
        return [r for r in restaurants if r.price_range in price_ranges]

    @staticmethod
    def filter_by_payment_method(
        restaurants: List[Restaurant],
        require_mobile_payment: bool = False,
        required_methods: List[PaymentMethod] = None,
    ) -> List[Restaurant]:
        """
        根據支付方式篩選

        Args:
            restaurants: 餐廳列表
            require_mobile_payment: 是否必須支援行動支付
            required_methods: 必須支援的支付方式列表（若指定則 require_mobile_payment 無效）

        Returns:
            篩選後的餐廳列表
        """
        if required_methods:
            return [
                r for r in restaurants
                if any(method in r.payment_methods for method in required_methods)
            ]

        if require_mobile_payment:
            return [r for r in restaurants if r.has_mobile_payment()]

        return restaurants

    @staticmethod
    def filter_by_active_status(
        restaurants: List[Restaurant], only_active: bool = True
    ) -> List[Restaurant]:
        """
        根據營業狀態篩選

        Args:
            restaurants: 餐廳列表
            only_active: 是否只顯示營業中的餐廳

        Returns:
            篩選後的餐廳列表
        """
        if only_active:
            return [r for r in restaurants if r.is_active]
        return restaurants

    @staticmethod
    def apply_filters(
        restaurants: List[Restaurant],
        center_lat: float,
        center_lon: float,
        max_distance_meters: int,
        price_ranges: List[PriceRange] = None,
        require_mobile_payment: bool = False,
        only_active: bool = True,
    ) -> List[Restaurant]:
        """
        套用所有篩選條件

        Args:
            restaurants: 餐廳列表
            center_lat, center_lon: 中心點座標（公司）
            max_distance_meters: 最大距離（公尺）
            price_ranges: 要篩選的價格範圍列表（None = 全部）
            require_mobile_payment: 是否必須支援行動支付
            only_active: 是否只顯示營業中的餐廳

        Returns:
            篩選後的餐廳列表
        """
        result = restaurants

        # 1. 篩選營業狀態
        result = FilterService.filter_by_active_status(result, only_active)

        # 2. 篩選距離
        result = GeometryService.filter_by_distance(
            result, center_lat, center_lon, max_distance_meters
        )

        # 3. 篩選價格
        if price_ranges:
            result = FilterService.filter_by_price_range(result, price_ranges)

        # 4. 篩選支付方式
        if require_mobile_payment:
            result = FilterService.filter_by_payment_method(
                result, require_mobile_payment=True
            )

        return result
