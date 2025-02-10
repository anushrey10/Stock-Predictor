import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    VERSION = '1.1.0'
    MODEL_UPDATE_INTERVAL = int(os.getenv('MODEL_UPDATE_INTERVAL', 86400))  # 24 hours
    MAX_HISTORICAL_DAYS = int(os.getenv('MAX_HISTORICAL_DAYS', 365 * 5))  # 5 years