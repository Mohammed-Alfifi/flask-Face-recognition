# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///EmployeeDB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mysecretkey'
class employee(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    hiringDate = db.Column(db.String(10), default=datetime.now().strftime("%d-%m-%Y"))
    def __repr__(self) -> str:
        return f"{self.id} - {self.name} - {self.department} - {self.email} - {self.hiringDate}"
# نموذج لقاعدة بيانات المستخدمين/المالك
class users(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=True)
    mail = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=True)
    def __repr__(self):
        return '<User {}>'.format(self.username)