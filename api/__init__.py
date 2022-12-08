# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask_migrate import Migrate

from . import v1
from .settings import configs
from .v1.models import db


def create_app(configName: str = "default"):
    app = Flask(
        import_name=__name__, 
        static_folder="../frontend/static",
        template_folder="../frontend"
    )
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://bookstore:bookstore@localhost:3306/bookstore"
    # # app.config["SQLALCHEMY_ECHO"] = True
    # app.config["JSON_AS_ASCII"] = False
    app.config.from_object(configs[configName])
    app.register_blueprint(
        v1.bp,
        url_prefix='/v1')
    db.init_app(app=app)
    Migrate(app=app, db=db)
    return app

if __name__ == '__main__':
    create_app().run(debug=True)