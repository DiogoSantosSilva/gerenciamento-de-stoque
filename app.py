# -*- coding: utf-8 _*_
from unittest import result
from flask import Flask, request, redirect, render_template
from config import app_config, app_active
from controller.User import UserController
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

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()

        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html',
                data={
                    'status': 401,
                    'msg': 'Dados de usuário incorretos',
                    'type': None
                }
            )

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Aqui entrará a tela de recuperar senha'

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()

        result = user.recovery(request.form['email'])

        if result:
            return render_template('recovery.html', 
            data={
                'status': 200,
                'msg': 'E-mail de recuperação enviado com sucesso!',
            })
        else:
            return render_template('recovery.html', 
            data={
                'status': 401,
                'msg': 'Erro  ao enviar E-mail de recuperação!',
            })


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
