import os

class Config:
    FLASK_DB = os.environ.get('FLASK_DB')