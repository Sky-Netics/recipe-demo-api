import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access token expires in 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)    # Refresh token expires in 30 days
    
    # Application
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Using same key for Flask sessions
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # Categories for recipes
    VALID_CATEGORIES = ['Breakfast', 'Lunch', 'Supper', 'Drinks']
