import os
import sys

# from dotenv import load_dotenv

from logger_costom import logger_email
from email_knd.core.config import email_client
from email_knd.core.constants import (
    ENV_EMAIL,
    ENV_EMAIL_SECURITY,
    ENV_SMTP_PORT,
    ENV_SMTP_SERVER,
    LOG_MSG_CHECK_ENV,
    LOG_MSG_EMAIL_NOT_SET,
    LOG_MSG_EMAIL_WORK_FINISHED,
    LOG_MSG_START_WORK,
)

# load_dotenv()


def main() -> None:
    """Основная функция: отправляет письмо и читает входящие."""
    logger_email.info(LOG_MSG_START_WORK)
    # Последовательный вызов функций отправки и чтения писем
    logger_email.info(f'Сообщение: {email_client.send_email()}')
    logger_email.info(f'Сообщение: {email_client.read_email()}')


if __name__ == '__main__':
    # Проверка наличия обязательных переменных окружения
    logger_email.debug(LOG_MSG_CHECK_ENV)
    if os.getenv(ENV_EMAIL) is None:
        logger_email.error(LOG_MSG_EMAIL_NOT_SET)
        sys.exit(1)
    # Логирование значений переменных окружения для отладки
    logger_email.debug(f'         EMAIL: {os.getenv(ENV_EMAIL)}')
    logger_email.debug(f'   SMTP_SERVER: {os.getenv(ENV_SMTP_SERVER)}')
    logger_email.debug(f'     SMTP_PORT: {os.getenv(ENV_SMTP_PORT)}')
    logger_email.debug(f'EMAIL_SECURITY: {os.getenv(ENV_EMAIL_SECURITY)}')

    # Запуск основной логики
    main()
    logger_email.info(LOG_MSG_EMAIL_WORK_FINISHED)
