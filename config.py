import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", 'waste2taste_projeect_test') 
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///waste2taste.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
