import os
import logging
from flask import Flask
from . import db, note, auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        logging.exception(str(e))

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(note.bp)
    app.add_url_rule('/', endpoint='index')

    return app