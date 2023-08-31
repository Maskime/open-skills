from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

user_company = db.Table('user_company',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                        db.Column('company_id', db.Integer, db.ForeignKey('companies.id'), primary_key=True))
user_technology = db.Table('user_technology',
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                           db.Column('technology_id', db.Integer, db.ForeignKey('technologies.id'), primary_key=True))
experience_technology = db.Table('experience_technology',
                                 db.Column('experience_id', db.Integer, db.ForeignKey('experiences.id'),
                                           primary_key=True),
                                 db.Column('technology_id', db.Integer, db.ForeignKey('technologies.id'),
                                           primary_key=True))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    experiences = db.relationship('Experience', lazy=True)
    technologies = db.relationship('Technology', secondary=user_technology, lazy='subquery')

    def __init__(self, email, password) -> None:
        super().__init__()
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional['User']:
        if not email or not password:
            return None
        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        return user


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

    users = db.relationship('User', secondary=user_company, lazy='subquery')
    experiences = db.relationship('Experience', lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'))


class Technology(db.Model):
    __tablename__ = 'technologies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Experience(db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    position = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    team_description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_current_position = db.Column(db.Boolean, nullable=False)
    tasks = db.relationship('Task', lazy=True)
