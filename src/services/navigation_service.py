"""
導航服務 - 生成 Google Maps 連結
"""
from typing import Optional
from urllib.parse import urlencode
from src.models.restaurant import Restaurant


class NavigationService:
    """導航服務"""

    GOOGLE_MAPS_BASE_URL = "https://maps.google.com"

    @staticmethod
    def generate_maps_link(
        latitude: float, longitude: float, name: Optional[str] = None
    ) -> str:
        """
        生成 Google Maps 連結

        Args:
            latitude: 緯度
            longitude: 經度
            name: 地點名稱（可選）

        Returns:
            Google Maps URL
        """
        params = {
            'q': f"{latitude},{longitude}",
        }

        if name:
            params['q'] = name  # 用名稱搜尋，會比較準確

        query_string = urlencode(params)
        return f"{NavigationService.GOOGLE_MAPS_BASE_URL}/maps?{query_string}"

    @staticmethod
    def generate_restaurant_maps_link(restaurant: Restaurant) -> str:
        """
        根據餐廳資訊生成 Google Maps 連結

        Args:
            restaurant: 餐廳物件

        Returns:
            Google Maps URL
        """
        if restaurant.google_maps_url:
            return restaurant.google_maps_url

        return NavigationService.generate_maps_link(
            restaurant.latitude, restaurant.longitude, restaurant.name
        )

    @staticmethod
    def generate_directions_link(
        from_lat: float,
        from_lon: float,
        to_lat: float,
        to_lon: float,
        to_name: Optional[str] = None,
    ) -> str:
        """
        生成 Google Maps 導航連結（從某地到某地）

        Args:
            from_lat, from_lon: 出發地座標
            to_lat, to_lon: 目的地座標
            to_name: 目的地名稱（可選）

        Returns:
            Google Maps 導航 URL
        """
        params = {
            'saddr': f"{from_lat},{from_lon}",
            'daddr': f"{to_lat},{to_lon}",
        }

        query_string = urlencode(params)
        return f"{NavigationService.GOOGLE_MAPS_BASE_URL}/maps?{query_string}"

    @staticmethod
    def generate_directions_from_company(
        from_lat: float,
        from_lon: float,
        restaurant: Restaurant,
    ) -> str:
        """
        生成從公司到餐廳的導航連結

        Args:
            from_lat, from_lon: 公司座標
            restaurant: 目的地餐廳

        Returns:
            Google Maps 導航 URL
        """
        return NavigationService.generate_directions_link(
            from_lat, from_lon, restaurant.latitude, restaurant.longitude, restaurant.name
        )
