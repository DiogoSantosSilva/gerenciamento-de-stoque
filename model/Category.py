# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from config import app_config, app_active

config = app_config[app_active]
db = SQLAlchemy(config.APP)


class Category(db.Model):
    """_summary_

    Args:
        db (_type_): _description_
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return self.name


    def get_total_categories(self):
        try:
            response = db.session.query(func.count(Category.id)).first()
        except Exception as error:
            print(error)
            response = []
        finally:
            db.session.close()
            return response
