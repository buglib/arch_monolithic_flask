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
from .resources.accounts import Accounts


routes = [
    dict(resource=Index, urls=['/index'], endpoint='index'),
    dict(resource=Advertisements, urls=['/advertisements'], endpoint='advertisements'),
    dict(resource=Products, urls=['/products'], endpoint='products'),
    dict(resource=Product, urls=['/products/<int:productId>'], endpoint='product'),
    dict(resource=Accounts, urls=['/accounts'], endpoint='accounts'),
]