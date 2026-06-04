"""
LINE Messaging API 事件處理器 V3 - 2026 AI 美食設計
"""
import json
from typing import Dict, Any, List
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent,
    TextSendMessage, FlexSendMessage
)
from src.config import get_config
from src.models.restaurant import PriceRange, PaymentMethod, PRICE_RANGE_INFO
from src.services.draw_service import DrawService
from src.services.navigation_service import NavigationService
from src.database.queries import get_all_restaurants

config = get_config()
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

# 2026 AI 美食設計配色
COLORS = {
    'primary': '#FF7A59',      # 暖橙色
    'primary_light': '#FF9A5F',
    'accent': '#FFB84D',       # 金黃
    'success': '#6FCF97',      # 柔和綠
    'dark': '#333333',
    'gray': '#999999',
    'light_bg': '#FAFAFA',
}

class LineHandlerV3:
    """LINE 事件處理器 V3 - 現代美食 AI 設計"""

    @staticmethod
    def handle_text_message(event: MessageEvent):
        """處理文字訊息"""
        text = event.message.text.strip()
        user_id = event.source.user_id
        trigger_words = ['午餐', '抽籤', 'lunch', 'draw']

        # 檢查是否包含觸發關鍵字（中文、英文皆可）
        should_trigger = False
        for word in trigger_words:
            if word in text:  # 完全字符匹配
                should_trigger = True
                break

        if should_trigger:
            LineHandlerV3.send_step1_distance_menu(user_id)
        else:
            reply_text = "👋 歡迎使用 AutoLunch 午餐探險家！\n\n輸入「午餐」或「抽籤」開始吧！"
            line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))

    @staticmethod
    def handle_postback(event: PostbackEvent):
        """處理 Postback 事件"""
        data = event.postback.data
        user_id = event.source.user_id

        if data == 'step1_restart':
            LineHandlerV3.send_step1_distance_menu(user_id)
        elif data.startswith('step1_'):
            LineHandlerV3.handle_step1_distance(user_id, data)
        elif data.startswith('step2_'):
            LineHandlerV3.handle_step2_price(user_id, data)
        elif data.startswith('step3_'):
            LineHandlerV3.handle_step3_payment(user_id, data)

    # ==================== Step 1: 距離選擇 ====================

    @staticmethod
    def send_step1_distance_menu(user_id: str):
        """發送第一步：距離選擇菜單 - 2026 AI 美食設計"""
        flex_message = FlexSendMessage(
            alt_text="Step 1/3: 選擇距離",
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": COLORS['primary'],
                    "paddingAll": "24px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🍜 午餐探險家",
                            "weight": "bold",
                            "size": "xxl",
                            "color": "#ffffff"
                        },
                        {
                            "type": "text",
                            "text": "AI 為你推薦美食",
                            "size": "sm",
                            "color": "rgba(255,255,255,0.8)",
                            "margin": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "lg",
                    "paddingAll": "24px",
                    "backgroundColor": COLORS['light_bg'],
                    "contents": [
                        {
                            "type": "text",
                            "text": "Step 1 - 你想走多遠？",
                            "weight": "bold",
                            "size": "xl",
                            "color": COLORS['dark']
                        },
                        {
                            "type": "text",
                            "text": "美食家的步行距離",
                            "size": "sm",
                            "color": COLORS['gray'],
                            "margin": "sm"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "🍽️ 300m (5分鐘) 上班最近",
                                        "data": "step1_select&distances=300"
                                    },
                                    "style": "primary",
                                    "color": COLORS['primary']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "🍲 500m (8分鐘) 輕鬆步行",
                                        "data": "step1_select&distances=500"
                                    },
                                    "style": "primary",
                                    "color": COLORS['primary_light']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "🥢 800m (12分鐘) 探險時間",
                                        "data": "step1_select&distances=800"
                                    },
                                    "style": "primary",
                                    "color": COLORS['accent']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "🍱 1km (15分鐘) 極限探險",
                                        "data": "step1_select&distances=1000"
                                    },
                                    "style": "primary",
                                    "color": "#FFC857"
                                }
                            ]
                        }
                    ]
                }
            }
        )
        line_bot_api.push_message(user_id, flex_message)

    @staticmethod
    def handle_step1_distance(user_id: str, data: str):
        """處理距離選擇"""
        params = dict(param.split('=') for param in data.split('&')[1:])
        distances = params.get('distances', '').split(',')
        distances = [int(d) for d in distances if d]
        LineHandlerV3.send_step2_price_menu(user_id, distances)

    # ==================== Step 2: 價格選擇 ====================

    @staticmethod
    def send_step2_price_menu(user_id: str, distances: List[int]):
        """發送第二步：價格選擇菜單"""
        distances_str = ','.join(map(str, distances))

        flex_message = FlexSendMessage(
            alt_text="Step 2/3: 選擇預算",
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": COLORS['primary'],
                    "paddingAll": "24px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "💰 選擇你的預算",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#ffffff"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "lg",
                    "paddingAll": "24px",
                    "backgroundColor": COLORS['light_bg'],
                    "contents": [
                        {
                            "type": "text",
                            "text": "Step 2 - 今天預算？",
                            "weight": "bold",
                            "size": "xl",
                            "color": COLORS['dark']
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💵 經濟美食 (50-100元)",
                                        "data": f"step2_select&distances={distances_str}&prices=economy"
                                    },
                                    "style": "primary",
                                    "color": COLORS['primary']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💳 中等品嚐 (150-250元)",
                                        "data": f"step2_select&distances={distances_str}&prices=cheap,mid"
                                    },
                                    "style": "primary",
                                    "color": COLORS['accent']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "👑 高檔享受 (400+元)",
                                        "data": f"step2_select&distances={distances_str}&prices=mid_high,premium"
                                    },
                                    "style": "primary",
                                    "color": "#FFB84D"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "✨ 不限預算",
                                        "data": f"step2_select&distances={distances_str}&prices=economy,cheap,mid,mid_high,premium"
                                    },
                                    "style": "primary",
                                    "color": COLORS['success']
                                }
                            ]
                        }
                    ]
                }
            }
        )
        line_bot_api.push_message(user_id, flex_message)

    @staticmethod
    def handle_step2_price(user_id: str, data: str):
        """處理價格選擇"""
        try:
            params = dict(param.split('=') for param in data.split('&')[1:])
            distances = params.get('distances', '').split(',')
            distances = [int(d) for d in distances if d]
            prices = params.get('prices', '').split(',')

            if not distances:
                line_bot_api.push_message(user_id, TextSendMessage(text="❌ 距離數據遺失，請重新選擇"))
                LineHandlerV3.send_step1_distance_menu(user_id)
                return

            LineHandlerV3.send_step3_payment_menu(user_id, distances, prices)
        except Exception as e:
            import logging
            logging.error(f"Step 2 error: {e}")
            line_bot_api.push_message(user_id, TextSendMessage(text="❌ 發生錯誤，請重新開始"))
            LineHandlerV3.send_step1_distance_menu(user_id)

    # ==================== Step 3: 支付選擇 ====================

    @staticmethod
    def send_step3_payment_menu(user_id: str, distances: List[int], prices: List[str]):
        """發送第三步：支付方式選擇菜單"""
        distances_str = ','.join(map(str, distances))
        prices_str = ','.join(prices)

        flex_message = FlexSendMessage(
            alt_text="Step 3/3: 選擇支付方式",
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": COLORS['primary'],
                    "paddingAll": "24px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "💳 選擇支付方式",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#ffffff"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "lg",
                    "paddingAll": "24px",
                    "backgroundColor": COLORS['light_bg'],
                    "contents": [
                        {
                            "type": "text",
                            "text": "Step 3 - 支付方式",
                            "weight": "bold",
                            "size": "xl",
                            "color": COLORS['dark']
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💰 現金",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=cash"
                                    },
                                    "style": "primary",
                                    "color": COLORS['primary']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📱 LINE Pay",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=line_pay"
                                    },
                                    "style": "primary",
                                    "color": COLORS['accent']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📱 街口支付",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=street_pay"
                                    },
                                    "style": "primary",
                                    "color": "#FFB84D"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "✨ 任何支付",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=cash,line_pay,street_pay"
                                    },
                                    "style": "primary",
                                    "color": COLORS['success']
                                }
                            ]
                        }
                    ]
                }
            }
        )
        line_bot_api.push_message(user_id, flex_message)

    @staticmethod
    def handle_step3_payment(user_id: str, data: str):
        """處理支付方式選擇，執行抽籤"""
        try:
            params = dict(param.split('=') for param in data.split('&')[1:])
            distances = params.get('distances', '').split(',')
            distances = [int(d) for d in distances if d]
            prices = params.get('prices', '').split(',')
            payments = params.get('payments', '').split(',')

            if not distances or not prices:
                line_bot_api.push_message(user_id, TextSendMessage(text="❌ 選擇不完整，請重新開始"))
                LineHandlerV3.send_step1_distance_menu(user_id)
                return

            confirm_text = f"✨ 準備抽籤中...\n\n📍 距離: {', '.join(map(str, distances))}m\n💰 預算: {', '.join(prices)}\n💳 支付: {', '.join(payments)}"
            line_bot_api.push_message(user_id, TextSendMessage(text=confirm_text))
            LineHandlerV3.perform_lucky_draw(user_id, distances, prices, payments)
        except Exception as e:
            import logging
            logging.error(f"Step 3 error: {e}")
            line_bot_api.push_message(user_id, TextSendMessage(text="❌ 發生錯誤，請重新開始"))
            LineHandlerV3.send_step1_distance_menu(user_id)

    # ==================== 結果：抽籤與顯示 ====================

    @staticmethod
    def perform_lucky_draw(user_id: str, distances: List[int], prices: List[str], payments: List[str]):
        """執行抽籤"""
        try:
            # 驗證參數
            if not distances or not prices:
                line_bot_api.push_message(user_id, TextSendMessage(
                    text="❌ 選擇不完整，請重新開始\n請點擊「再抽一次」或輸入「午餐」重新選擇"
                ))
                LineHandlerV3.send_step1_distance_menu(user_id)
                return

            all_restaurants = get_all_restaurants()

            if not all_restaurants:
                line_bot_api.push_message(user_id, TextSendMessage(text="❌ 找不到任何餐廳"))
                return

            from src.models.restaurant import PriceRange

            filtered_restaurants = []
            max_distance = max(distances)

            price_enums = [PriceRange(p) for p in prices if p]

            for restaurant in all_restaurants:
                if not restaurant.distance or restaurant.distance > max_distance:
                    continue

                distance_ok = any(restaurant.distance <= d for d in distances)
                if not distance_ok:
                    continue

                if restaurant.price_range not in price_enums:
                    continue

                payment_ok = False
                if not payments or payments == ['']:
                    payment_ok = True
                else:
                    # 支付方式映射（從前端代碼到 PaymentMethod 值）
                    payment_map = {
                        'cash': PaymentMethod.CASH.value,
                        'line_pay': PaymentMethod.LINE_PAY.value,
                        'street_pay': PaymentMethod.STREET_CASH.value
                    }
                    required_payment_values = [payment_map.get(p, '') for p in payments if p]
                    restaurant_payment_values = [p.value for p in restaurant.payment_methods]

                    # 檢查餐廳是否支持選定的支付方式之一
                    for required_value in required_payment_values:
                        if required_value in restaurant_payment_values:
                            payment_ok = True
                            break

                if not payment_ok:
                    continue

                filtered_restaurants.append(restaurant)

            if not filtered_restaurants:
                line_bot_api.push_message(user_id, TextSendMessage(
                    text="❌ 沒有符合條件的餐廳\n請調整選擇條件重試"
                ))
                return

            selected = DrawService.lucky_draw(filtered_restaurants)

            if not selected:
                line_bot_api.push_message(user_id, TextSendMessage(text="❌ 抽籤失敗"))
                return

            maps_url = NavigationService.generate_restaurant_maps_link(selected)

            detail_contents = [
                {
                    "type": "text",
                    "text": f"📍 {selected.distance:.0f}m 步行{int(selected.distance/80)}分鐘",
                    "size": "sm",
                    "color": COLORS['gray']
                },
                {
                    "type": "text",
                    "text": f"💰 {PRICE_RANGE_INFO.get(selected.price_range.value, {}).get('name', selected.price_range.value)}",
                    "size": "sm",
                    "color": COLORS['gray']
                }
            ]

            if selected.rating > 0:
                detail_contents.append({
                    "type": "text",
                    "text": f"⭐ {selected.rating} 星評分",
                    "size": "sm",
                    "color": COLORS['gray']
                })

            result_card = {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": COLORS['primary'],
                    "paddingAll": "24px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎉 恭喜！",
                            "weight": "bold",
                            "size": "xxl",
                            "color": "#ffffff"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "paddingAll": "24px",
                    "backgroundColor": COLORS['light_bg'],
                    "contents": [
                        {
                            "type": "text",
                            "text": "你的午餐是...",
                            "size": "sm",
                            "color": COLORS['gray']
                        },
                        {
                            "type": "text",
                            "text": selected.name,
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md",
                            "color": COLORS['primary']
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": detail_contents
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "📍 Google Maps",
                                        "uri": maps_url
                                    },
                                    "style": "primary",
                                    "color": COLORS['success']
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "🎲 再抽一次",
                                        "data": "step1_restart"
                                    },
                                    "style": "secondary"
                                }
                            ]
                        }
                    ]
                }
            }

            flex_message = FlexSendMessage(alt_text=f"你的午餐是: {selected.name}", contents=result_card)
            line_bot_api.push_message(user_id, flex_message)

        except Exception as e:
            import logging
            logging.error(f"抽籤錯誤: {e}")
            line_bot_api.push_message(user_id, TextSendMessage(text=f"❌ 發生錯誤: {str(e)}"))
