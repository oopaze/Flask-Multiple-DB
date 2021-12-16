from flask import Blueprint, redirect, url_for, render_template_string, request
from flask_login import login_user, current_user
from flask_login.utils import login_required, logout_user

from .utils import (
    LOGIN_FORM,
    generate_random_user,
)
from app.src.database import db
from .models import UserUE, UserBR


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def create_a_random_user():
    generate_random_user()

    return redirect(url_for('user.login'))


@user_blueprint.route('/register/<int:number_of_users>', methods=['GET', 'POST'])
def create_a_number_of_random_users(number_of_users=1):
    for _ in range(number_of_users):
        generate_random_user()

    return redirect(url_for('user.list_user'))


@user_blueprint.route('/list/<type>')
@user_blueprint.route('/list/')
def list_user(type=None):
    if type == 'br':
        users = UserBR.query.all()
    elif type == 'eu':
        users = UserUE.query.all()
    else:
        users_brazilian = list(UserBR.query.all())
        users_europe = list(UserUE.query.all())
        users = users_brazilian + users_europe

    return "<br>".join([f"{user}" for user in users])


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Do not make it in production, this is too unsecurity
    if request.method == 'POST':
        username = request.values.get('username', '')
        password = request.values.get('password', '')

        try:
            instance = UserUE.get(username)

            if instance.verify_password(password):
                login_user(instance)

                instance.is_authenticated = True
                db.session.commit()

                return redirect(url_for('user.logout'))

        except UserUE.UserNotFoundError as e:
            print(e)

    return render_template_string(LOGIN_FORM)


@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    return render_template_string("Você está logado {{ current_user }}")
