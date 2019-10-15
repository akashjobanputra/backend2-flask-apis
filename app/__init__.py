from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from . import errors
from config import config

db = SQLAlchemy()


def create_app(config_name, *args, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    errors.set_errors(app)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/')
    def index():
        return redirect('/apidocs')

    return app
