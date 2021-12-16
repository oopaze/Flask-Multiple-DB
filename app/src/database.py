from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.core.models import BaseModel


db = SQLAlchemy(model_class=BaseModel)
migrate = Migrate()


def configure_db(app):
    db.init_app(app)
    migrate.init_app(app, db)

    app.db = db
