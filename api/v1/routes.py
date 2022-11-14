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


routes = [
    dict(resource=Index, urls=['/index'], endpoint=''),
    dict(resource=Advertisements, urls=['/advertisements'], endpoint='advertisements'),
]