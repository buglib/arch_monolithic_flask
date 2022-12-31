# coding: utf-8
import time

from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2TokenMixin
)
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

    def get_user_id(self):
        return self.id

    def check_password(self, password: str):
        return password == self.password


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


# class Oauth2Client(db.Model):
#     __tablename__ = 'oauth2_client'

#     client_id = db.Column(db.String(48), index=True)
#     client_secret = db.Column(db.String(120))
#     client_id_issued_at = db.Column(db.Integer, nullable=False)
#     client_secret_expires_at = db.Column(db.Integer, nullable=False)
#     client_metadata = db.Column(db.Text)
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.ForeignKey('account.id', ondelete='CASCADE'), nullable=False, index=True)

#     user = db.relationship('Account', primaryjoin='Oauth2Client.user_id == Account.id', backref='oauth2_clients')

class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = "oauth2_client"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("account.id", ondelete="CASCADE"))
    user = db.relationship("Account")

    # @property
    # def token_endpoint_auth_method(self):
    #     return self.client_metadata.get(
    #         'token_endpoint_auth_method',
    #         'none'
    #     )


# class Oauth2Token(db.Model):
#     __tablename__ = 'oauth2_token'

#     client_id = db.Column(db.String(48))
#     token_type = db.Column(db.String(40))
#     access_token = db.Column(db.String(1024), nullable=False, unique=True)
#     refresh_token = db.Column(db.String(1024), index=True)
#     scope = db.Column(db.Text)
#     issued_at = db.Column(db.Integer, nullable=False)
#     access_token_revoked_at = db.Column(db.BigInteger, nullable=False)
#     refresh_token_revoked_at = db.Column(db.BigInteger, nullable=False)
#     expires_in = db.Column(db.Integer, nullable=False)
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.ForeignKey('account.id', ondelete='CASCADE'), index=True)

#     user = db.relationship('Account', primaryjoin='Oauth2Token.user_id == Account.id', backref='oauth2_tokens')

class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = "oauth2_token"

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(512), unique=True, nullable=False)
    refresh_token = db.Column(db.String(512), index=True)
    access_token_revoked_at = db.Column(db.BigInteger, nullable=False, default=0)
    refresh_token_revoked_at = db.Column(db.BigInteger, nullable=False, default=0)
    expires_in = db.Column(db.BigInteger, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id", ondelete="CASCADE"))
    user = db.relationship("Account")

    def is_refresh_token_active(self):
        expires_at = self.issued_at + self.expires_in
        return expires_at >= time.time()