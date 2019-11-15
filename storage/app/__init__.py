from flask import Flask
from .config import Config
from .db.reset_db import reset_db
from os import getenv

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    reset_db(app.config['FLASK_DB'], bool(int(getenv("RESET_DB", "0"))))

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
