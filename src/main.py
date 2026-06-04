"""
AutoLunch LINE 午餐抽籤機器人 - 主應用
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, abort
from src.config import get_config
from src.database.queries import init_db, get_all_restaurants
from src.handlers.line_handler_v2 import (
    line_bot_api, webhook_handler, LineHandlerV2 as LineHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent

# 初始化應用
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# 初始化資料庫
init_db()

# 檢查並初始化資料（Render 上自動運行）
try:
    restaurants_count = len(get_all_restaurants())
    if restaurants_count == 0:
        # 如果資料庫是空的，自動初始化
        import subprocess
        import sys
        from pathlib import Path

        script_path = Path(__file__).parent.parent / 'scripts' / 'fetch_restaurants_overpass.py'
        if script_path.exists():
            # 使用 Overpass API 抓取餐廳
            subprocess.run([sys.executable, str(script_path)], timeout=300)
        else:
            # 備選：使用示範資料
            script_path = Path(__file__).parent.parent / 'scripts' / 'populate_sample_data.py'
            if script_path.exists():
                subprocess.run([sys.executable, str(script_path)])
except Exception as e:
    import logging
    logging.warning(f"Could not initialize data: {e}")


@app.before_request
def before_request():
    """請求前處理"""
    pass


@app.after_request
def after_request(response):
    """請求後處理"""
    return response


@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return {
        'status': 'healthy',
        'service': 'AutoLunch LINE Bot',
        'version': '1.0.0',
    }, 200


@app.route('/debug', methods=['GET'])
def debug_info():
    """診斷端點 - 檢查配置和數據"""
    import os

    try:
        restaurants = get_all_restaurants()

        return {
            'status': 'ok',
            'environment': {
                'PYTHONIOENCODING': os.getenv('PYTHONIOENCODING'),
                'FLASK_ENV': os.getenv('FLASK_ENV'),
                'DATABASE_URL': os.getenv('DATABASE_URL', 'Not set'),
            },
            'database': {
                'total_restaurants': len(restaurants),
                'sample_restaurant': {
                    'name': restaurants[0].name if restaurants else None,
                    'distance': restaurants[0].distance if restaurants else None,
                    'price_range': str(restaurants[0].price_range) if restaurants else None,
                } if restaurants else None,
            },
            'config': {
                'company_name': config.COMPANY_NAME,
                'company_location': f"{config.COMPANY_LATITUDE}, {config.COMPANY_LONGITUDE}",
                'distance_options': config.DISTANCE_OPTIONS,
            }
        }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
        }, 500


@app.route('/webhook/line', methods=['POST'])
def webhook():
    """
    LINE Webhook 端點
    接收來自 LINE 的事件
    """
    signature = request.headers.get('X-Line-Signature')

    if not signature:
        abort(400)

    body = request.get_data(as_text=True)

    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(403)

    return 'OK', 200


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """處理文字訊息"""
    LineHandler.handle_text_message(event)


@webhook_handler.add(PostbackEvent)
def handle_postback(event):
    """處理 Postback 事件"""
    LineHandler.handle_postback(event)


@app.errorhandler(400)
def bad_request(error):
    """400 錯誤處理"""
    return {'error': 'Bad request'}, 400


@app.errorhandler(403)
def forbidden(error):
    """403 錯誤處理"""
    return {'error': 'Forbidden'}, 403


@app.errorhandler(404)
def not_found(error):
    """404 錯誤處理"""
    return {'error': 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    """500 錯誤處理"""
    return {'error': 'Internal server error'}, 500


def main():
    """主函數"""
    import logging

    # 設定日誌
    logging.basicConfig(level=config.LOG_LEVEL)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting AutoLunch Bot...")
    logger.info(f"Company: {config.COMPANY_NAME}")
    logger.info(f"Location: {config.COMPANY_LATITUDE}, {config.COMPANY_LONGITUDE}")
    logger.info(f"Distance options: {config.DISTANCE_OPTIONS}")

    # 啟動伺服器
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG,
    )


if __name__ == '__main__':
    main()
