import os
from datetime import timedelta

SECRET_KEY = "secret-key"

JWT_SECRET_KEY = "jwt-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR,
        "database",
        "tma.db"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "secret-key"
    JWT_SECRET_KEY = "jwt-secret-key"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False