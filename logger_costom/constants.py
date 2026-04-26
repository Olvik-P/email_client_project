# ===== Логирование (loguru) =====
# Настройка логера
LOG_FORMAT = (
    '<level>{level: <8}</level>  '
    '<green>{time:YYYY-MM-DD HH:mm:ss}</green> '
    '{extra} '
    ' <level>{message}</level>'
)
LOG_FILE = 'logs/log_email.log'
LOG_LEVEL_DEV = 'DEBUG'
LOG_LEVEL_PROD = 'INFO'
LOG_ROTATION = '10 MB'
LOG_RETENTION = '7 days'
LOG_USE_CONSOLE = True
LOG_ENCODING = 'utf-8'

# ===== Если пользователь не определен =====
LOG_STR_SYSTEM_NAME = 'SYSTEM'
LOG_VALUE_ZERO = 0
