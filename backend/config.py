import os

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

    SQLALCHEMY_TRACK_MODIFICATIONS = False