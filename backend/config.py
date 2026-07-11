import os
from datetime import timedelta


class Config:
    SECRET_KEY = "to-be-added"
    JWT_SECRET_KEY = "secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    #abs. path to backend directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "trekking.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False