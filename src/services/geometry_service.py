"""
地理計算服務 - 距離計算和地理篩選
"""
import math
from typing import List, Tuple
from src.models.restaurant import Restaurant


class GeometryService:
    """地理計算服務"""

    EARTH_RADIUS_METERS = 6371000  # 地球半徑（公尺）

    @staticmethod
    def haversine_distance(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        使用 Haversine 公式計算兩點間的距離（公尺）

        Args:
            lat1, lon1: 起點（公司）座標
            lat2, lon2: 終點（餐廳）座標

        Returns:
            距離（公尺）
        """
        # 轉換為弧度
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        # Haversine 公式
        a = (
            math.sin(delta_phi / 2) ** 2 +
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        distance = GeometryService.EARTH_RADIUS_METERS * c

        return round(distance, 1)

    @staticmethod
    def filter_by_distance(
        restaurants: List[Restaurant],
        center_lat: float,
        center_lon: float,
        max_distance_meters: int,
    ) -> List[Restaurant]:
        """
        根據距離篩選餐廳

        Args:
            restaurants: 餐廳列表
            center_lat, center_lon: 中心點座標（公司）
            max_distance_meters: 最大距離（公尺）

        Returns:
            篩選後的餐廳列表（已包含距離）
        """
        filtered = []

        for restaurant in restaurants:
            distance = GeometryService.haversine_distance(
                center_lat,
                center_lon,
                restaurant.latitude,
                restaurant.longitude,
            )

            if distance <= max_distance_meters:
                restaurant.distance = distance
                filtered.append(restaurant)

        # 按距離排序
        filtered.sort(key=lambda r: r.distance)

        return filtered

    @staticmethod
    def get_walking_time_estimate(distance_meters: float) -> str:
        """
        估計步行時間

        Args:
            distance_meters: 距離（公尺）

        Returns:
            步行時間估計（文字）
        """
        # 成人平均步行速度：1.4 m/s ≈ 5 km/h
        # 計算時間（分鐘）
        minutes = int(distance_meters / 1.4 / 60)

        if minutes < 1:
            return "1 分鐘以內"
        elif minutes <= 5:
            return f"約 {minutes} 分鐘"
        elif minutes <= 15:
            return f"約 {minutes} 分鐘"
        elif minutes <= 30:
            return f"約 {minutes} 分鐘"
        else:
            return f"約 {minutes} 分鐘（{distance_meters/1000:.1f} km）"
