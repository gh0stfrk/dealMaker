from .database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    code = db.Column(db.String(100), unique=True)
    initial_price = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
