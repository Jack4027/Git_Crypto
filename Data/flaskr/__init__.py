import os
from flask import Flask
from .dashboard import create

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app = create(app) #creating dash app

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import display
    app.register_blueprint(display.bp)
    app.add_url_rule('/', endpoint='index')
    return app
