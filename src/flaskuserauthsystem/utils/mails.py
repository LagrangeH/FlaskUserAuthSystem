import datetime

from flask_mail import Message, email_dispatched
from loguru import logger as log

from src.flaskuserauthsystem import mail
from src.flaskuserauthsystem.database.recovery_link import RecoveryLink
from src.flaskuserauthsystem.database.user import User


def send_mail(recovery_link: RecoveryLink, user: User, host='http://127.0.0.1:5000') -> None:
    # TODO: add connection error handling
    # log.debug(f'Sending mail to {recovery_link}. Token: /restore-password/{recovery_link.link_token}')

    body = f"Dear {user.username},\n\n" \
           f"We received a request to reset your password for your account. " \
           f"To proceed with the password reset, please follow the link below:\n\n" \
           f"{host}/auth/recover-password/{recovery_link.link_token}\n\n" \
           f"If you did not request this password reset, please ignore this email.\n\n" \
           f"Thank you for using our service."

    msg = Message(
        subject="Password Recovery for Flask User Auth System",
        recipients=['lagrange2718@gmail.com'],
        body=body,
    )

    mail.send(msg)
