from app.src.database import db
from app.core.models import BaseUser


class UserBR(BaseUser, db.Model):
    __tablename__ = 'br_usuarios'
    __bind_key__ = 'brazil'

    def __str__(self):
        """Função que retona a represenção em string da classe"""
        return f"{self.username} - Brazilian User ({self.id})"

    def __repr__(self):
        """Função que retornar a saida de um print do nosso objeto"""
        return f'<Brazilian User {self.username}>'


class UserUE(BaseUser, db.Model):
    __tablename__ = 'ue_usuarios'
    __bind_key__ = 'europe'
    resume = db.Column(db.Text, nullable=True)

    def __init__(self, *args, resume: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.resume = resume

    def __str__(self):
        """Função que retona a represenção em string da classe"""
        return f"{self.username} - Europe User ({self.id})"

    def __repr__(self):
        """Função que retornar a saida de um print do nosso objeto"""
        return f'<Europe User {self.username}>'
