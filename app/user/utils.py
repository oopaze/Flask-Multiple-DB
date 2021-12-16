from random import choices, choice
from string import ascii_letters, digits

from flask import current_app

from app.user.models import UserBR, UserUE


CHARACTERS = ascii_letters + digits


def generate_random_user():
    user_class = choice([UserBR, UserUE])

    first_name = generate_random_name()
    last_name = generate_random_name()

    complete_name = f"{first_name} {last_name}"
    username = f"{first_name}_{last_name}"
    password = generate_random_password()

    print(password, username)

    instance_kw = {'name': complete_name, 'username': username, 'password': password}

    if user_class == UserUE:
        instance_kw['resume'] = generate_random_resume()

    instance = user_class(**instance_kw)

    current_app.db.session.add(instance)
    current_app.db.session.commit()


def generate_random_name():
    return "".join(choices(ascii_letters, k=10))


def generate_random_resume():
    return "".join(choices(ascii_letters, k=300))


def generate_random_password():
    return "".join(choices(CHARACTERS, k=10))


LOGIN_FORM = """
    <form method='POST' action='{{ url_for('user.login') }}'>
        <input type='text' name='username' placeholder='Username'>
        <input type='password' name='password' placeholder='Password'>
        <input type='submit' value='Login'>
    </form>
"""


LOGIN_CREDENTIALS = {"password": "YHreriD8nx", "username": "CbaOVDGCeT_fkgJNHRYTO"}
