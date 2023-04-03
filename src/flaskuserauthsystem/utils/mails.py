from loguru import logger as log

from src.flaskuserauthsystem.database.recovery_link import RecoveryLink


def send_mail(recovery_link: RecoveryLink) -> None:
    log.debug(f'Sending mail to {recovery_link}. Token: /restore-password/{recovery_link.link_token}')
