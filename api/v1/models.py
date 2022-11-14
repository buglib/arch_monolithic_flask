# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    location = db.Column(db.String(100))



class Advertisement(db.Model):
    __tablename__ = 'advertisement'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    product_id = db.Column(db.ForeignKey('product.id', ondelete='CASCADE'), index=True)

    product = db.relationship('Product', primaryjoin='Advertisement.product_id == Product.id', backref='advertisements')



class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    pay_id = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)
    total_price = db.Column(db.Numeric(10, 0))
    expires = db.Column(db.Integer, nullable=False)
    payment_link = db.Column(db.String(300))
    pay_state = db.Column(db.String(20))



class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    price = db.Column(db.Numeric(10, 0))
    rate = db.Column(db.Float)
    description = db.Column(db.String(8000))
    cover = db.Column(db.String(100))
    detail = db.Column(db.String(100))



class Specification(db.Model):
    __tablename__ = 'specification'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50))
    value = db.Column(db.String(100))
    product_id = db.Column(db.ForeignKey('product.id', ondelete='CASCADE'), index=True)

    product = db.relationship('Product', primaryjoin='Specification.product_id == Product.id', backref='specifications')



class Stockpile(db.Model):
    __tablename__ = 'stockpile'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    frozen = db.Column(db.Integer)
    product_id = db.Column(db.ForeignKey('product.id', ondelete='CASCADE'), index=True)

    product = db.relationship('Product', primaryjoin='Stockpile.product_id == Product.id', backref='stockpiles')



class Wallet(db.Model):
    __tablename__ = 'wallet'

    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Numeric(10, 0))
    account_id = db.Column(db.ForeignKey('account.id', ondelete='CASCADE'), index=True)

    account = db.relationship('Account', primaryjoin='Wallet.account_id == Account.id', backref='wallets')
