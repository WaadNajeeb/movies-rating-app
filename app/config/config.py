import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))



class Config:
    """Base configuration class with common settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')  # Change this in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy event system
    SQLALCHEMY_ECHO = False  #  to log all SQL queries
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')  # Can be 'production', 'development', etc.



class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '..', 'database', 'movies_db.sqlite')}"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''  # Set this in production


class TestingConfig(Config):
    """Testing-specific configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''


# Map environment variables to config classes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}