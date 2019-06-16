from typing import Any

from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base

db: Any = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(postgresql.INTEGER, primary_key=True)
    name = db.Column(postgresql.VARCHAR(12), unique=True)
    description = db.Column(postgresql.VARCHAR(255))

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.email

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
