# -*- coding: utf-8 _*_
from flask import Flask, request
from config import app_config, app_active
from flask_sqlalchemy import SQLAlchemy

config = app_config[app_active]
db = SQLAlchemy(config.APP)
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def create_app(config_name):

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Meu primeiro run'

    @app.route('/login/')
    def login():
        return 'Aqui entrará a tela de login'

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Aqui entrará a tela de recuperar senha'

    # @app.route('/profile/<int:user_id>/')
    # def profile(user_id):
    #     return 'O ID desse usuário é %d', user_id

    @app.route('/profile/<int:user_id>/action/<action>/')
    def profile(user_id, action):
        return 'Ação %s usuáro de ID %d', action, user_id

    @app.route('/profile/', methods=['POST', 'GET'])
    def create_profile():
        username = request.form['username']
        password = request.form['password']

        return f"""Essa rota possui um método POST e criará um usuário com os
            dados de usuário {username} e senha {password} """

    @app.route('/profile/<int:user_id>/', methods=['PUT'])
    def edit_total_profile(user_id):
        username = request.form['username']
        password = request.form['password']

        return 'Essa rota possui um método PUT e editará um usuário com os ' \
               'dados de usuário %s e senha %s', username, password

    return app
