from datetime import datetime

from sqlalchemy.exc import StatementError
from sqlalchemy.orm import synonym

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import Model
from flask_sqlalchemy.model import sa
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(Model):
    criado_em = sa.Column(sa.DateTime, default=datetime.now)
    atualizado_em = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.id)
                break
        else:
            type = sa.Integer

        return sa.Column(type, primary_key=True)


class BaseUser(Model):
    __abstract__ = True
    name = sa.Column(sa.String, nullable=True)
    password = sa.Column(sa.String, nullable=False)
    admin = sa.Column(sa.Boolean, default=False)
    username = sa.Column(sa.String, unique=True, nullable=False)

    # manage login
    is_authenticated = sa.Column(sa.Boolean, default=False)

    class UserNotFoundError(Exception):
        DEFAULT_MESSAGE = "Usuário não encontrado na nossa base de dados"

        def __init__(self, message=None, *args, **kwargs):
            message = message or self.DEFAULT_MESSAGE
            super().__init__(message, *args, **kwargs)

    def __init__(self, name, username, password, admin: bool = None):
        self.name = name
        self._username = username
        self.password = self.generate_hash_password(password)

        if admin:
            self.admin = admin

    @property
    def is_active(self):
        return True

    @declared_attr
    def _username(self):
        return synonym('username', descriptor=property(fset=self.set_username))

    def set_username(self, value):
        try:
            instance = self.get(username=value)

            if instance:
                raise StatementError('Já existe um usuário com esse username')

        except ValueError:
            raise StatementError('Já existem usuários com esse username')

        except self.UserNotFoundError:
            pass

        self.username = value

    @classmethod
    def get(cls, username):
        from app.user.models import UserUE, UserBR

        ue_instance = UserUE.query.filter_by(username=username).first()
        br_instance = UserBR.query.filter_by(username=username).first()

        if br_instance and ue_instance:
            raise ValueError('Multiple Object Returned.')

        elif not (br_instance or ue_instance):
            raise cls.UserNotFoundError

        return br_instance or ue_instance

    def get_id(self):
        """Método usado pelo Login Manager com o objetivo de usar o username no login"""
        return self.username

    def generate_hash_password(self, password):
        """Função responsável por encriptar o password do usuario"""
        return generate_password_hash(password)

    def verify_password(self, password):
        """Função responsável por comparar os passwords encriptados do usuario"""
        return check_password_hash(self.password, password)
