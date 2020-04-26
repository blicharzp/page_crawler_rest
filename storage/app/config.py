import os
from os import environ

class Config:
    REDIS_URL = "redis://:@{}:{}/0".format(environ.get('DB_SERVICE_NAME', ""), 
                                           environ.get('DB_SERVICE_PORT', ""))
