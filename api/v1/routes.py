# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .resources.index import Index
from .resources.advertisements import Advertisements
from .resources.products import Products
from .resources.product import Product
from .resources.products_stockpile import ProductsStockpile
from .resources.accounts import Accounts
from .resources.accounts_username import AccountsUsername
from .resources.oauth_token import OauthToken


routes = [
    dict(resource=Index, urls=['/index'], endpoint='index'),
    dict(resource=Advertisements, urls=['/advertisements'], endpoint='advertisements'),
    dict(resource=Products, urls=['/products'], endpoint='products'),
    dict(resource=Product, urls=['/products/<int:productId>'], endpoint='product'),
    dict(resource=ProductsStockpile, urls=['/products/stockpile/<int:productId>'], endpoint='products_stockpile_product'),
    dict(resource=Accounts, urls=['/accounts'], endpoint='accounts'),
    dict(resource=AccountsUsername, urls=['/accounts/<username>'], endpoint='accounts_username'),
    dict(resource=OauthToken, urls=['/oauth/token'], endpoint='oauth_token'),
]