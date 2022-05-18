import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://tellem:123qwerty@localhost/team4'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    DEBUG = True


    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://tellem:123qwerty@localhost/team4'
 
  
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://tellem:123qwerty@localhost/team4_test'

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}