from unittest import result
from model.User import User

class UserController():
    def __init__(self):
        self.user_model = User()

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

    def recovery(email):
        return ''