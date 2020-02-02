import sqlalchemy as sa
from sqlalchemy_mixins import AllFeaturesMixin
from app import app, db


class BaseModel(db.Model, AllFeaturesMixin):
    __abstract__ = True
    pass

BaseModel.set_session(db.session)


class User(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(30), unique=True)
    password = sa.Column(sa.String(18))
    email = sa.Column(sa.String(30), unique=True, nullable=True)
    mobile = sa.Column(sa.String(30), unique=True, nullable=True)
    # dob = sa.Column(sa.String(10), nullable=True)
    # gender = sa.Column(sa.String(10), nullable=True)


class Post(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    content = sa.Column(sa.Text)

    user = sa.orm.relationship('User', backref='posts')

    
class Comment(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True)
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    body = sa.Column(sa.Text)

    post = sa.orm.relationship('Post', backref='comments')
    user = sa.orm.relationship('User', backref='comments')


class Like(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True)
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))

    post = sa.orm.relationship('Post', backref='likes')
    user = sa.orm.relationship('User', backref='likes')
