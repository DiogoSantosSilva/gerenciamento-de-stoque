from datetime import datetime, timedelta
import hashlib, base64, json, jwt
from config import app_config, app_active
from model.User import User

from controller.Email import EmailController

config = app_config[app_active]


class UserController:
    def __init__(self):
        self.user_model = User()
        self.email_controller = EmailController()

    def get_user_by_id(self, user_id):
        result = {}
        try:
            self.user_model.id = user_id
            user = self.user_model.get_user_by_id()
            result = {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "date_created": user.date_created
            }
            status = 200
        except Exception as error:
            print(error)
            result = []
            status: 400
        finally:
            return {
                "result": result,
                "status": status
            }

    def login(self, email, password):
        """Get the email data and save in the model

        Args:
            email (str): user email
            password (str): user password
        """

        self.user_model.email = email
        result = self.user_model.get_user_by_email()
        if result is not None:
            res = self.user_model.verify_password(password, result.password)

            if res:
                return result
            else:
                return {}
        return {}

    def recovery(self, to_email):
        self.user_model.email = to_email
        response = self.user_model.get_user_by_email()
        if response is not None:
            user_id = response.id
            username = response.username
            recovery_code = self.generate_auth_token({
                "id": user_id,
                "username": username,
            }, exp=5)
            recovery_code = recovery_code.encode("ascii").decode("utf-8")
            try:
                self.user_model.id = response.id
                response = self.user_model.update({
                    "recovery_code": recovery_code
                })

                if response:
                    content_text = f"Olá {username}. Para realizar a alteração de senha, você precisa acessar a " \
                                   f"seguinte url: {config.URL_MAIN}new-password/{recovery_code}"
                else:
                    return {
                        "status_code": 401,
                        "body": "Erro ao gerar código de envio",
                    }
            except Exception as error:
                print(error)
                return {
                    "status_code": 401,
                    "body": "Erro ao gerar código de envio",
                }

            try:
                result = self.email_controller.send_email(to_email, "Recuperação de senha", content_text)
            except Exception as error:
                print(error)
                return {
                    "status_code": 401,
                    "body": "Erro no serviço de e-mail. Por favor. Entre em contato com o administrador",
                }
        else:
            return {
                "status_code": 401,
                "body": "Usuário inexistente",
            }
        return result

    def get_user_by_recovery(self, recovery_password):
        self.user_model.recovery_code = recovery_password
        return self.user_model.get_user_by_recovery()

    def new_password(self, user_id, password):
        self.user_model.set_password(password)
        self.user_model.id = user_id

        return self.user_model.update({
            "password": self.user_model.password
        })

    def verify_auth_token(self, access_token):
        status = 401
        try:
            jwt.decode(access_token,  config.SECRET, algorithms='HS256')
            message = "Token válido"
            status = 200
        except jwt.ExpiredSignatureError as error:
            print(error)
            message = "Token expirado, realize um novo login"
        except Exception as error:
            print(error)
            message = "Token inválido"

        return {
            "message": message,
            "status": status
        }

    def generate_auth_token(self, data, exp=30, time_exp=False):
        if time_exp:
            date_time = data["exp"]
        else:
            date_time = datetime.utcnow() + timedelta(minutes=exp)

        dict_jwt = {
            "id": data["id"],
            "username": data['username'],
            "exp": date_time
        }

        access_token = jwt.encode(dict_jwt, config.SECRET, algorithm="HS256")

        return access_token

    def get_admin_login(self, user_id):
        self.user_model.id = user_id

        response = self.user_model.get_user_by_id()
        return response

