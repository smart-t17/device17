import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "thisisasecretkey")
    NIAGARA4_SERVER = os.getenv("NIAGARA4_SERVER", "")  # type: str
    NIAGARA4_USERNAME = os.getenv("NIAGARA4_USERNAME", "")  # type: str
    NIAGARA4_PASSWORD = os.getenv("NIAGARA4_PASSWORD", "")  # type: str

    # set color for admin page
    FLASK_ADMIN_SWATCH = "cerulean"


class LocalConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = "postgres://localhost/device17"
    NIAGARA4_SERVER = "https://34.203.113.170:443"
    NIAGARA4_USERNAME = "daniel"
    NIAGARA4_PASSWORD = "daniel2"


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://localhost/device17_test"
    )
    NIAGARA4_SERVER = "https://34.203.113.170:443"
    NIAGARA4_USERNAME = "daniel"
    NIAGARA4_PASSWORD = "daniel2"


class StagingConfig(Config):
    LOG_LEVEL = "INFO"


class ProductionConfig(Config):
    LOG_LEVEL = "INFO"
