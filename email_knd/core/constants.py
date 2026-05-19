from pathlib import Path
from datetime import datetime

ATTACHMENTS_DIR = Path(__file__).parent.parent.parent / 'Programms'
SENDER_UNKNOWN = 'Unknown'
SENDER_EMAIL = 'nadzor-knd@egov66.ru'  # От кого письмо
RECIPIENT_EMAIL = 'olpon0@yandex.ru'  # Кому посылаем
MESSAGE_SUBJECT = 'Программа проверок'  
ATTACHMENT_FILENAME = 'Программа проверок.pdf'

LOG_MSG_SENDED = 'Настраиваем отправку емаил ...'
LOG_MSG_SENDED_SUCCESS = 'Настроили, отправляем ...'
LOG_MSG_SEND_OK = 'Письмо успешно отправлено: recipient = {recipient}'
LOG_MSG_SEND_ERROR = 'Ошибка при отправке: {error}'
LOG_MSG_EMAIL_READ = 'Настраиваем чтение емаил ...'
LOG_MSG_NEW_MAIL_NOT_FOUND = 'Новых писем не найдено'

# Константы для письма
TEST_MESSAGE_SUBJECT = f'Тестовое письмо от {datetime.today()}'
TEST_MESSAGE_BODY = f'Привет! Сегодня {datetime.today()} и это тестовое письмо из моей программы!'

# Константы статусов
STATUS_OK = 'ok'
STATUS_ERROR = 'error'
STATUS_EMPTY = 'empty'
EMAIL_SENDED = 'sended'
EMAIL_NOT_SENDED = 'not sended'

# Константы IMAP
IMAP_INBOX = 'INBOX'
IMAP_SEARCH_UNSEEN = 'UNSEEN'

# Числовые константы
INITIAL_FILES_COUNT = 0

# Дополнительные константы для логов
LOG_MSG_EMAIL_SUITABLE = 'Письмо подходит'
LOG_MSG_SKIP_ATTACHMENT = 'Пропускаем вложение: {filename}'
LOG_MSG_START_WORK = 'Начало работы ...'
LOG_MSG_CHECK_ENV = 'Проверка переменные окружения ...'
LOG_MSG_EMAIL_NOT_SET = 'EMAIL не установлен в переменных окружения'
LOG_MSG_EMAIL_WORK_FINISHED = 'Работа с емаил окончена.'

# Константы для переменных окружения
ENV_EMAIL = 'EMAIL'
ENV_SMTP_SERVER = 'SMTP_SERVER'
ENV_SMTP_PORT = 'SMTP_PORT'
ENV_EMAIL_SECURITY = 'EMAIL_SECURITY'

MAX_SIZE = 10 * 1024 * 1024
