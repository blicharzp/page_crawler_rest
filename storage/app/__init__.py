from flask import Flask
from .config import Config
from os import getenv


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .db import db

    db.init_app(app)

    return app
