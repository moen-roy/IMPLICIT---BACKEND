# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    # General Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS =  True

    # JWT settings
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 'False').lower() == 'true'
    JWT_IDENTITY_CLAIM = os.getenv('JWT_IDENTITY_CLAIM')