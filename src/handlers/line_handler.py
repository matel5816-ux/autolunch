"""
LINE Messaging API 事件處理器
"""
from typing import Dict, Any
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent,
    TextSendMessage, FlexSendMessage
)
from src.config import get_config
from src.models.restaurant import PriceRange, PaymentMethod
from src.services.filter_service import FilterService
from src.services.draw_service import DrawService
from src.services.navigation_service import NavigationService
from src.database.queries import get_all_restaurants

config = get_config()

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(config.LINE_CHANNEL_SECRET)


class LineHandler:
    """LINE 事件處理器"""

    @staticmethod
    def handle_text_message(event: MessageEvent):
        """
        處理文字訊息

        Args:
            event: LINE 訊息事件
        """
        text = event.message.text.strip()
        user_id = event.source.user_id

        # 觸發詞
        trigger_words = ['午餐', '抽籤', 'lunch', 'draw']

        if any(text.lower() in word.lower() or word.lower() in text.lower()
               for word in trigger_words):
            LineHandler.send_filter_menu(user_id)
        else:
            # 預設回應
            reply_text = "👋 歡迎使用 AutoLunch 午餐抽籤機！\n\n" \
                        "輸入「午餐」或「抽籤」開始選擇午餐地點吧！"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    @staticmethod
    def handle_postback(event: PostbackEvent):
        """
        處理 Postback 事件（Flex Message 按鈕點擊）

        Args:
            event: Postback 事件
        """
        data = event.postback.data
        user_id = event.source.user_id

        # 解析 Postback 資料
        # 格式：distance=1000&price=mid&payment=true
        params = dict(param.split('=') for param in data.split('&'))

        distance = int(params.get('distance', 1000))
        price = params.get('price', 'all')  # all, budget, mid, premium
        require_payment = params.get('payment', 'false').lower() == 'true'

        LineHandler.perform_lucky_draw(user_id, event.reply_token, distance, price, require_payment)

    @staticmethod
    def send_filter_menu(user_id: str):
        """
        發送篩選選單 Flex Message

        Args:
            user_id: LINE 使用者 ID
        """
        flex_message = FlexSendMessage(
            alt_text="請選擇午餐篩選條件",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🍜 午餐抽籤",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1DB446"
                        },
                        {
                            "type": "text",
                            "text": "選擇你的午餐條件吧！",
                            "size": "sm",
                            "color": "#999999",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📍 距離",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#666666"
                                },
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "action": {
                                        "type": "postback",
                                        "label": "🚶 300m (4分鐘)",
                                        "data": "distance=300&price=all&payment=false"
                                    }
                                },
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "action": {
                                        "type": "postback",
                                        "label": "🚶‍♂️ 600m (7-8分鐘)",
                                        "data": "distance=600&price=all&payment=false"
                                    }
                                },
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "action": {
                                        "type": "postback",
                                        "label": "🚴 1km (13-15分鐘)",
                                        "data": "distance=1000&price=all&payment=false"
                                    }
                                },
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "action": {
                                        "type": "postback",
                                        "label": "🚴‍♂️ 1.5km (18-20分鐘)",
                                        "data": "distance=1500&price=all&payment=false"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        )

        line_bot_api.push_message(user_id, flex_message)

    @staticmethod
    def perform_lucky_draw(
        user_id: str,
        reply_token: str,
        distance: int,
        price: str,
        require_payment: bool,
    ):
        """
        執行隨機抽籤

        Args:
            user_id: LINE 使用者 ID
            reply_token: 回覆令牌
            distance: 距離（公尺）
            price: 價格範圍（all, budget, mid, premium）
            require_payment: 是否要求支持行動支付
        """
        try:
            # 取得所有餐廳
            all_restaurants = get_all_restaurants()

            # 確定價格篩選
            price_ranges = []
            if price == 'all':
                price_ranges = [PriceRange.BUDGET, PriceRange.MID, PriceRange.PREMIUM]
            elif price == 'budget':
                price_ranges = [PriceRange.BUDGET]
            elif price == 'mid':
                price_ranges = [PriceRange.MID]
            elif price == 'premium':
                price_ranges = [PriceRange.PREMIUM]

            # 套用篩選
            filtered = FilterService.apply_filters(
                all_restaurants,
                config.COMPANY_LOCATION['latitude'],
                config.COMPANY_LOCATION['longitude'],
                distance,
                price_ranges=price_ranges,
                require_mobile_payment=require_payment,
            )

            if not filtered:
                # 沒有符合條件的餐廳
                reply_text = "😅 沒有符合條件的餐廳呢\n\n請試試調整篩選條件吧！"
                line_bot_api.reply_message(
                    reply_token, TextSendMessage(text=reply_text)
                )
                return

            # 隨機抽籤
            winner = DrawService.lucky_draw(filtered)

            if not winner:
                reply_text = "😅 發生錯誤，請重試"
                line_bot_api.reply_message(
                    reply_token, TextSendMessage(text=reply_text)
                )
                return

            # 生成 Google Maps 連結
            maps_link = NavigationService.generate_restaurant_maps_link(winner)

            # 生成結果卡片
            result_message = LineHandler.create_result_card(winner, maps_link)
            line_bot_api.reply_message(reply_token, result_message)

        except Exception as e:
            print(f"Error in lucky draw: {str(e)}")
            reply_text = "❌ 發生錯誤，請重試"
            line_bot_api.reply_message(
                reply_token, TextSendMessage(text=reply_text)
            )

    @staticmethod
    def create_result_card(winner, maps_link: str) -> FlexSendMessage:
        """
        建立抽籤結果卡片

        Args:
            winner: 獲勝的餐廳
            maps_link: Google Maps 連結

        Returns:
            Flex Message
        """
        price_emoji = {
            'budget': '💰',
            'mid': '💰💰',
            'premium': '💰💰💰',
        }

        emoji = price_emoji.get(winner.price_range.value, '💰')

        return FlexSendMessage(
            alt_text=f"🎉 抽籤結果：{winner.name}",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎉 抽籤結果",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#FF6B6B"
                        },
                        {
                            "type": "text",
                            "text": winner.name,
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md",
                            "color": "#1DB446"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "距離",
                                            "color": "#aaaaaa",
                                            "size": "sm",
                                            "flex": 1
                                        },
                                        {
                                            "type": "text",
                                            "text": f"{winner.distance:.0f}m",
                                            "wrap": True,
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 5
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "預算",
                                            "color": "#aaaaaa",
                                            "size": "sm",
                                            "flex": 1
                                        },
                                        {
                                            "type": "text",
                                            "text": f"{emoji} {winner.price_range.value}",
                                            "wrap": True,
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "📍 Google Maps",
                                "uri": maps_link
                            },
                            "style": "link",
                            "height": "sm",
                            "margin": "lg"
                        }
                    ]
                }
            }
        )
