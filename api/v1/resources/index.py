# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import sys

from flask import render_template, Response, jsonify, current_app

from . import Resource
from ..models import (
    Advertisement
)

class Index(Resource):

    def get(self):
        resp = Response(
            response=render_template("index.html"),
            content_type="text/html; charset=utf-8",
            status=200
        )
        return resp
