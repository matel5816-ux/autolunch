"""
AutoLunch 配置管理
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """基礎配置"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # LINE Bot
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

    # Google APIs
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')

    # Company Info
    COMPANY_NAME = os.getenv('COMPANY_NAME', '群健科技 Cofit')
    COMPANY_LATITUDE = float(os.getenv('COMPANY_LATITUDE', '25.0638409'))
    COMPANY_LONGITUDE = float(os.getenv('COMPANY_LONGITUDE', '121.5334954'))

    COMPANY_LOCATION = {
        'name': COMPANY_NAME,
        'latitude': COMPANY_LATITUDE,
        'longitude': COMPANY_LONGITUDE,
    }

    # Distance Options
    DISTANCE_OPTIONS = [
        int(d) for d in os.getenv('DISTANCE_OPTIONS', '300,600,1000,1500').split(',')
    ]
    DEFAULT_DISTANCE = int(os.getenv('DEFAULT_DISTANCE', '1000'))

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data/restaurants.db')

    # Feature Flags
    ENABLE_DISTANCE_VALIDATION = os.getenv('ENABLE_DISTANCE_VALIDATION', 'True') == 'True'
    ENABLE_RICH_MENU = os.getenv('ENABLE_RICH_MENU', 'False') == 'True'

    # Performance
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', '100'))
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '30'))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'


def get_config():
    """根據環境變數取得對應配置"""
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
