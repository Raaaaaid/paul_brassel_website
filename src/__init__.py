
from flask import Flask
from flask_bootstrap import Bootstrap

from config import config
from .main import main as main_blueprint


def create_app(config_name):
    app = Flask(__name__)

    # Configure application.
    c = config[config_name]
    app.config.from_object(c)

    # Initialize extensions.
    Bootstrap(app=app)
    c.init_app(app)

    # Register blueprint.
    app.register_blueprint(main_blueprint)

    return app
