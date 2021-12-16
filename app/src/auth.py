from flask_login import LoginManager

from app.core.models import BaseUser


login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.id_attribute = 'get_id'


def configure_login(app):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return BaseUser.get(user_id)
