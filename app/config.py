import os
import pymysql
import urllib.parse


class Config(object):
    password = urllib.parse.quote_plus('qweQWE123!@#')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret:)'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://devops:{password}@85.234.107.240/dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False