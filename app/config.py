import os
import pymysql
import urllib.parse


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TGSTAT_TOKEN = os.environ.get('TGSTAT_TOKEN') or 'tokentokentokentokentokentokento'

    KEYWORDS = '(word|word2) -(banword1|banword2)'

    password = urllib.parse.quote_plus('db_password')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://username:password@127.0.0.1/db_name'
