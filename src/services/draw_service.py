"""
隨機抽籤服務
"""
import random
from typing import List, Optional
from src.models.restaurant import Restaurant


class DrawService:
    """隨機抽籤服務"""

    @staticmethod
    def lucky_draw(restaurants: List[Restaurant]) -> Optional[Restaurant]:
        """
        從餐廳列表中隨機抽一間

        Args:
            restaurants: 篩選後的餐廳列表

        Returns:
            隨機選中的餐廳，若列表為空則回傳 None
        """
        if not restaurants:
            return None

        return random.choice(restaurants)

    @staticmethod
    def multiple_draws(
        restaurants: List[Restaurant], count: int = 3
    ) -> List[Restaurant]:
        """
        從餐廳列表中隨機抽多間（不重複）

        Args:
            restaurants: 篩選後的餐廳列表
            count: 要抽的數量

        Returns:
            隨機選中的餐廳列表
        """
        if not restaurants:
            return []

        draw_count = min(count, len(restaurants))
        return random.sample(restaurants, draw_count)

    @staticmethod
    def weighted_draw(
        restaurants: List[Restaurant], use_rating: bool = True
    ) -> Optional[Restaurant]:
        """
        基於評分的加權隨機抽籤（評分高的餐廳被選中的機率較高）

        Args:
            restaurants: 篩選後的餐廳列表
            use_rating: 是否使用評分作為權重

        Returns:
            隨機選中的餐廳，若列表為空則回傳 None
        """
        if not restaurants:
            return None

        if not use_rating or all(r.rating == 0 for r in restaurants):
            return random.choice(restaurants)

        # 使用評分作為權重（+ 1 確保即使評分為 0 也有機會被選中）
        weights = [r.rating + 1 for r in restaurants]
        return random.choices(restaurants, weights=weights, k=1)[0]
