import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import app_config, app_active

config = app_config[app_active]


class EmailController:

    def send_email(self, to_email, subject, content_text, from_email="diogo.ds62@gmail.com"):

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content_text
        )
        try:
            sendgrid_client = SendGridAPIClient(config.SENDGRID_API_KEY)
            response = sendgrid_client.send(message)

            return {
                "status_code": response.status_code,
                "body": response.body,
                "headers": response.headers
            }
        except Exception as error:
            print(error.reason)
            raise error