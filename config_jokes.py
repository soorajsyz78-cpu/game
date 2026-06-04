import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    DEFAULT_API = os.getenv('DEFAULT_API', 'jokeapi')
    ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    CACHE_DURATION = int(os.getenv('CACHE_DURATION', '3600'))  # 1 hour
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '5'))  # 5 seconds

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    ENABLE_CACHE = False

# Determine which config to use
config_name = os.getenv('FLASK_ENV', 'development')
if config_name == 'production':
    config = ProductionConfig()
elif config_name == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
