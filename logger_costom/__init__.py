import os

from logger_costom.costom_loguru import LoggerLoguru

logger_email = LoggerLoguru.create()

is_dev = os.getenv('ENV_TYPE', 'dev') == 'dev'

if is_dev:
    logger_email.info(
        'Режим разработки: логирование настроено для вывода в консоль.'
    )
else:
    logger_email.info(
        'Режим продакшена: логирование настроено для вывода в консоль и файл.'
    )

__all__ = ['logger_email']
