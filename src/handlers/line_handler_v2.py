"""
LINE Messaging API 事件處理器 V2 - 多步式多選菜單
"""
import json
from typing import Dict, Any, List, Optional
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent,
    TextSendMessage, FlexSendMessage
)
from src.config import get_config
from src.models.restaurant import PriceRange, PaymentMethod, PRICE_RANGE_INFO
from src.services.filter_service import FilterService
from src.services.draw_service import DrawService
from src.services.navigation_service import NavigationService
from src.database.queries import get_all_restaurants

config = get_config()

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(config.LINE_CHANNEL_SECRET)


class LineHandlerV2:
    """LINE 事件處理器 V2"""

    @staticmethod
    def handle_text_message(event: MessageEvent):
        """處理文字訊息"""
        text = event.message.text.strip()
        user_id = event.source.user_id

        trigger_words = ['午餐', '抽籤', 'lunch', 'draw']

        if any(text.lower() in word.lower() or word.lower() in text.lower()
               for word in trigger_words):
            LineHandlerV2.send_step1_distance_menu(user_id)
        else:
            reply_text = "👋 歡迎使用 AutoLunch 午餐抽籤機！\n\n" \
                        "輸入「午餐」或「抽籤」開始選擇午餐地點吧！"
            line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))

    @staticmethod
    def handle_postback(event: PostbackEvent):
        """處理 Postback 事件"""
        data = event.postback.data
        user_id = event.source.user_id

        if data.startswith('step1_'):
            LineHandlerV2.handle_step1_distance(user_id, data)
        elif data.startswith('step2_'):
            LineHandlerV2.handle_step2_price(user_id, data)
        elif data.startswith('step3_'):
            LineHandlerV2.handle_step3_payment(user_id, data)
        elif data.startswith('result_'):
            LineHandlerV2.handle_result_draw(user_id, data)

    # ==================== Step 1: 距離選擇 ====================

    @staticmethod
    def send_step1_distance_menu(user_id: str):
        """發送第一步：距離選擇菜單"""
        flex_message = FlexSendMessage(
            alt_text="Step 1/3: 選擇距離",
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🍜 AutoLunch",
                            "weight": "bold",
                            "size": "xxl",
                            "color": "#ffffff"
                        },
                        {
                            "type": "text",
                            "text": "午餐抽籤機",
                            "size": "lg",
                            "color": "#ffffff",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#1DB446",
                    "paddingAll": "20px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Step 1/3",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0
                                },
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "text",
                                    "text": "距離範圍",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": "你想在多遠的地方吃午餐？",
                            "weight": "bold",
                            "size": "lg",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📍 300m (5-10分鐘)",
                                        "data": "step1_select&distances=300"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📍 600m (10-15分鐘)",
                                        "data": "step1_select&distances=600"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📍 1km (15-20分鐘)",
                                        "data": "step1_select&distances=1000"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📍 1.5km (20-25分鐘)",
                                        "data": "step1_select&distances=1500"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📍 不限距離",
                                        "data": "step1_select&distances=300,600,1000,1500"
                                    },
                                    "style": "primary",
                                    "color": "#FF6B6B"
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

        LineHandlerV2.send_step2_price_menu(user_id, distances)

    # ==================== Step 2: 價格選擇 ====================

    @staticmethod
    def send_step2_price_menu(user_id: str, distances: List[int]):
        """發送第二步：價格選擇菜單"""
        distances_str = ','.join(map(str, distances))

        flex_message = FlexSendMessage(
            alt_text="Step 2/3: 選擇價格",
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🍜 AutoLunch",
                            "weight": "bold",
                            "size": "xxl",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": "#1DB446",
                    "paddingAll": "20px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Step 2/3",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0
                                },
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "text",
                                    "text": "預算範圍",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": "你的預算是多少？",
                            "weight": "bold",
                            "size": "lg",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💵 經濟 (50-100元)",
                                        "data": f"step2_select&distances={distances_str}&prices=economy"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💵💵 平價 (100-150元)",
                                        "data": f"step2_select&distances={distances_str}&prices=cheap"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💵💵💵 中等 (150-250元)",
                                        "data": f"step2_select&distances={distances_str}&prices=mid"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💵💵💵💵 中高 (250-400元)",
                                        "data": f"step2_select&distances={distances_str}&prices=mid_high"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💵💵💵💵💵 高檔 (400+元)",
                                        "data": f"step2_select&distances={distances_str}&prices=premium"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "✅ 不限預算",
                                        "data": f"step2_select&distances={distances_str}&prices=economy,cheap,mid,mid_high,premium"
                                    },
                                    "style": "primary",
                                    "color": "#FF6B6B"
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
        params = dict(param.split('=') for param in data.split('&')[1:])
        distances = params.get('distances', '').split(',')
        distances = [int(d) for d in distances if d]
        prices = params.get('prices', '').split(',')

        LineHandlerV2.send_step3_payment_menu(user_id, distances, prices)

    # ==================== Step 3: 付款方式選擇 ====================

    @staticmethod
    def send_step3_payment_menu(user_id: str, distances: List[int], prices: List[str]):
        """發送第三步：付款方式選擇菜單"""
        distances_str = ','.join(map(str, distances))
        prices_str = ','.join(prices)

        flex_message = FlexSendMessage(
            alt_text="Step 3/3: 選擇付款方式",
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🍜 AutoLunch",
                            "weight": "bold",
                            "size": "xxl",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": "#1DB446",
                    "paddingAll": "20px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Step 3/3",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0
                                },
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "text",
                                    "text": "付款方式",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": "你想用什麼方式付款？",
                            "weight": "bold",
                            "size": "lg",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "💰 現金",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=cash"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📱 LINE Pay",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=line_pay"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "📱 街口支付",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=street_pay"
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "✅ 任何付款",
                                        "data": f"step3_select&distances={distances_str}&prices={prices_str}&payments=cash,line_pay,street_pay"
                                    },
                                    "style": "primary",
                                    "color": "#FF6B6B"
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
        """處理付款方式選擇，發送確認和開始抽籤"""
        params = dict(param.split('=') for param in data.split('&')[1:])
        distances = params.get('distances', '').split(',')
        distances = [int(d) for d in distances if d]
        prices = params.get('prices', '').split(',')
        payments = params.get('payments', '').split(',')

        # 發送確認信息
        confirm_text = f"✅ 條件已設定\n\n"
        confirm_text += f"📍 距離: {', '.join(map(str, distances))}公尺\n"
        confirm_text += f"💵 價格: {', '.join(prices)}\n"
        confirm_text += f"💰 支付: {', '.join(payments)}\n\n"
        confirm_text += "🎲 準備抽籤..."

        line_bot_api.push_message(user_id, TextSendMessage(text=confirm_text))

        # 立即執行抽籤
        LineHandlerV2.perform_lucky_draw(user_id, distances, prices, payments)

    # ==================== 結果：抽籤與顯示 ====================

    @staticmethod
    def perform_lucky_draw(user_id: str, distances: List[int], prices: List[str], payments: List[str]):
        """執行抽籤"""
        try:
            # 獲取所有餐廳
            all_restaurants = get_all_restaurants()

            if not all_restaurants:
                line_bot_api.push_message(user_id, TextSendMessage(text="❌ 抱歉，找不到任何餐廳"))
                return

            # 過濾符合條件的餐廳
            from src.models.restaurant import PriceRange

            filtered_restaurants = []
            max_distance = max(distances)

            # 將字符串價格轉換為 Enum
            price_enums = []
            for p in prices:
                try:
                    price_enums.append(PriceRange(p))
                except:
                    pass

            for restaurant in all_restaurants:
                # 檢查距離
                if not restaurant.distance or restaurant.distance > max_distance:
                    continue

                # 檢查距離是否在選定範圍內
                distance_ok = any(restaurant.distance <= d for d in distances)
                if not distance_ok:
                    continue

                # 檢查價格
                if restaurant.price_range not in price_enums:
                    continue

                # 檢查支付方式
                payment_ok = False
                if not payments or payments == ['']:
                    payment_ok = True
                else:
                    payment_map = {
                        'cash': '現金',
                        'line_pay': 'LINE Pay',
                        'street_pay': '街口支付'
                    }
                    for payment in payments:
                        payment_name = payment_map.get(payment, '')
                        if payment_name in [p.value for p in restaurant.payment_methods]:
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

            # 隨機抽籤
            selected = DrawService.lucky_draw(filtered_restaurants)

            if not selected:
                line_bot_api.push_message(user_id, TextSendMessage(text="❌ 抽籤失敗"))
                return

            # 生成 Google Maps URL
            maps_url = NavigationService.generate_restaurant_maps_link(selected)

            # 發送結果卡片
            detail_contents = [
                {
                    "type": "text",
                    "text": f"📍 距離: {selected.distance:.0f}m",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": f"💵 價格: {PRICE_RANGE_INFO.get(selected.price_range, {}).get('name', selected.price_range)}",
                    "size": "sm"
                }
            ]

            if selected.rating > 0:
                detail_contents.append({
                    "type": "text",
                    "text": f"⭐ 評分: {selected.rating}",
                    "size": "sm"
                })

            if selected.phone:
                detail_contents.append({
                    "type": "text",
                    "text": f"📞 {selected.phone}",
                    "size": "xs",
                    "color": "#999999"
                })

            result_card = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎉 恭喜！",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#FF6B6B"
                        },
                        {
                            "type": "text",
                            "text": "你的午餐是...",
                            "size": "sm",
                            "color": "#999999"
                        },
                        {
                            "type": "text",
                            "text": selected.name,
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md",
                            "color": "#1DB446"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "spacing": "sm",
                            "contents": detail_contents
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "📍 Google Maps",
                                        "uri": maps_url
                                    },
                                    "style": "primary",
                                    "color": "#1DB446"
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

            flex_message = FlexSendMessage(alt_text=f"抽籤結果: {selected.name}", contents=result_card)
            line_bot_api.push_message(user_id, flex_message)

        except Exception as e:
            import logging
            logging.error(f"抽籤錯誤: {e}")
            line_bot_api.push_message(user_id, TextSendMessage(text=f"❌ 發生錯誤: {str(e)}"))
