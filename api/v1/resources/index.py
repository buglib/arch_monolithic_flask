# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import render_template, Response

from . import Resource
from .. import schemas


class Index(Resource):

    def get(self):
        # return render_template("index.html"), 200, {"Content-Type": "text/html; charset=utf-8"}
        resp = Response(
            response=render_template("index.html"),
            content_type="text/html; charset=utf-8",
            status=200
        )
        return resp