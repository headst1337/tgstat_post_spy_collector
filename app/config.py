import os
from dotenv import load_dotenv


load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TGSTAT_TOKEN = os.environ.get('TGSTAT_TOKEN')
    KEYWORDS = os.environ.get('KEYWORDS')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
