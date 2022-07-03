# -*- coding: utf-8 -*-
from app import db
from config import app_config, app_active

config = app_config[app_active]


class Category(db.Model):
    """_summary_

    Args:
        db (_type_): _description_
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)