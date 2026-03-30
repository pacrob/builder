from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    from app.auth import auth_bp
    from app.entries import entries_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(entries_bp)

    return app
