import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", 'this-is-a-super-long-and-unchanging-secret-key')  # Change in production
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///waste2taste.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
