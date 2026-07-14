import os
from datetime import timedelta


class Config:
    SECRET_KEY = "secret-key"
    JWT_SECRET_KEY = "jwtsecret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    #abs. path to backend directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "trekking.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #celery configuration
    CELERY = {
        "broker_url": "redis://localhost:6379/0",
        "result_backend": "redis://localhost:6379/0",
    }
    #mails
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")