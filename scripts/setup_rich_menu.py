"""
設置 LINE Rich Menu（菜單按鈕）
讓用戶可以直接點擊按鈕，不用輸入「午餐」
"""
import sys
import os
import json
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import get_config

config = get_config()

def setup_rich_menu():
    """設置 Rich Menu"""

    # Rich Menu 配置
    rich_menu = {
        "size": {
            "width": 2500,
            "height": 810
        },
        "selected": True,
        "name": "AutoLunch Menu",
        "chatBarText": "🍜 午餐抽籤",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 833,
                    "height": 810
                },
                "action": {
                    "type": "postback",
                    "data": "step1_select&distances=300"
                }
            },
            {
                "bounds": {
                    "x": 833,
                    "y": 0,
                    "width": 833,
                    "height": 810
                },
                "action": {
                    "type": "postback",
                    "data": "step1_select&distances=500"
                }
            },
            {
                "bounds": {
                    "x": 1666,
                    "y": 0,
                    "width": 834,
                    "height": 810
                },
                "action": {
                    "type": "postback",
                    "data": "step1_select&distances=800"
                }
            }
        ]
    }

    # LINE API 端點
    line_api_url = "https://api.line.me/v2/bot/richmenu"
    headers = {
        "Authorization": f"Bearer {config.LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    print("📱 正在設置 Rich Menu...")

    try:
        # 建立 Rich Menu
        response = requests.post(
            line_api_url,
            headers=headers,
            json=rich_menu
        )

        if response.status_code == 200:
            rich_menu_id = response.json().get('richMenuId')
            print(f"✅ Rich Menu 已建立！ID: {rich_menu_id}")

            # 上傳 Rich Menu 圖片
            image_path = os.path.join(
                os.path.dirname(__file__),
                'rich_menu_image.png'
            )

            if os.path.exists(image_path):
                upload_rich_menu_image(rich_menu_id, image_path)
                print(f"✅ Rich Menu 圖片已上傳")
            else:
                print(f"⚠️ Rich Menu 圖片未找到 ({image_path})")
                print(f"   請手動上傳一張 2500x810 的圖片")

            # 設為預設菜單
            set_default_rich_menu(rich_menu_id)
            print(f"✅ Rich Menu 已設為預設菜單")

        else:
            print(f"❌ 建立失敗: {response.status_code}")
            print(f"   {response.text}")

    except Exception as e:
        print(f"❌ 錯誤: {e}")


def upload_rich_menu_image(rich_menu_id: str, image_path: str):
    """上傳 Rich Menu 圖片"""
    from src.config import get_config
    config = get_config()

    url = f"https://api.line.me/v2/bot/richmenu/{rich_menu_id}/image"
    headers = {
        "Authorization": f"Bearer {config.LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "image/png"
    }

    try:
        with open(image_path, 'rb') as f:
            response = requests.post(
                url,
                headers=headers,
                data=f
            )

        if response.status_code in [200, 204]:
            print(f"✅ 圖片已上傳")
        else:
            print(f"❌ 上傳失敗: {response.status_code}")

    except Exception as e:
        print(f"❌ 錯誤: {e}")


def set_default_rich_menu(rich_menu_id: str):
    """設置預設 Rich Menu"""
    from src.config import get_config
    config = get_config()

    url = f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}"
    headers = {
        "Authorization": f"Bearer {config.LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print(f"✅ 已設為預設菜單")
        else:
            print(f"❌ 設置失敗: {response.status_code}")

    except Exception as e:
        print(f"❌ 錯誤: {e}")


if __name__ == '__main__':
    setup_rich_menu()
