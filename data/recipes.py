import sqlalchemy
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    image = sqlalchemy.Column(sqlalchemy.String, default='/static/img/none-user-image.png')
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    products = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    difficult = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    likes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)