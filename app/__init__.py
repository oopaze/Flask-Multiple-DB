from flask import Flask

from app.src.auth import configure_login

from .src.database import configure_db
from .user.routes import user_blueprint


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Development')

    configure_db(app)
    configure_login(app)

    app.register_blueprint(user_blueprint)

    return app


app = create_app()
