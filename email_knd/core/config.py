import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from MailToolsBox import EmailSender, ImapClient
from dotenv import load_dotenv

from email_knd.core.constants import (
    ATTACHMENTS_DIR,
    ATTACHMENT_FILENAME,
    EMAIL_NOT_SENDED,
    EMAIL_SENDED,
    IMAP_INBOX,
    IMAP_SEARCH_UNSEEN,
    INITIAL_FILES_COUNT,
    LOG_MSG_EMAIL_READ,
    LOG_MSG_EMAIL_SUITABLE,
    LOG_MSG_NEW_MAIL_NOT_FOUND,
    LOG_MSG_SENDED,
    LOG_MSG_SENDED_SUCCESS,
    LOG_MSG_SEND_ERROR,
    LOG_MSG_SEND_OK,
    LOG_MSG_SKIP_ATTACHMENT,
    MAX_SIZE,
    MESSAGE_SUBJECT,
    RECIPIENT_EMAIL,
    SENDER_EMAIL,
    SENDER_UNKNOWN,
    STATUS_EMPTY,
    STATUS_ERROR,
    STATUS_OK,
    TEST_MESSAGE_BODY,
    TEST_MESSAGE_SUBJECT,
)
from logger_costom import logger_email

load_dotenv()


class EmailKndClient:
    """Клиент для работы с электронной почтой в рамках проекта KND.

    Обеспечивает отправку тестовых писем и чтение непрочитанных писем
    с сохранением подходящих вложений.
    """

    def __init__(self) -> None:
        """Инициализирует клиенты для отправки и получения почты.

        Создает экземпляры EmailSender и ImapClient из переменных окружения.
        """
        try:
            self.send_client = EmailSender.from_env()
            self.imap_client = ImapClient.from_env()
        except Exception as e:
            logger_email.error(f"Ошибка инициализации клиентов: {e}")
            raise

    def send_email(
            self,
            subject: str = TEST_MESSAGE_SUBJECT,
            message_body: str = TEST_MESSAGE_BODY
    ) -> Dict[str, str]:
        """Отправляет тестовое письмо с конфигурацией из окружения."""
        logger_email.info(LOG_MSG_SENDED)
        send = self.send_client
        logger_email.info(LOG_MSG_SENDED_SUCCESS)
        try:
            send.send(
                recipients=[RECIPIENT_EMAIL],
                subject=subject,
                message_body=message_body
            )
            logger_email.info(
                LOG_MSG_SEND_OK.format(recipient=RECIPIENT_EMAIL))
        except Exception as e:
            logger_email.error(
                LOG_MSG_SEND_ERROR.format(error=e),
                exc_info=True
            )
            return {'status': STATUS_ERROR, 'email': EMAIL_NOT_SENDED}

        return {'status': STATUS_OK, 'email': EMAIL_SENDED}

    def _validate_attachment(self, file_data: bytes, filename: str) -> bool:
        """Проверяет вложение на соответствие критериям PDF.

        Проверяет сигнатуру '%PDF', размер (не более 10 МБ) и минимальную
        длину. Возвращает True, если вложение валидно, иначе False.
        """
        logger_email.debug(f'Проверка вложения {filename} ...')

        # Проверка на пустые данные
        if not file_data:
            logger_email.info(f'Вложение {filename} пустое')
            return False

        # Проверка размера (10 МБ = 10 * 1024 * 1024 байт)
        if len(file_data) > MAX_SIZE:
            logger_email.info(
                f'Вложение {filename} превышает максимальный размер 10 МБ'
            )
            return False

        # Проверка минимальной длины для сигнатуры
        if len(file_data) < 4:
            logger_email.info(
                f'Вложение {filename} слишком мало для проверки сигнатуры'
            )
            return False

        # Проверка сигнатуры PDF (первые 4 байта должны быть '%PDF')
        # Некоторые PDF могут начинаться с '%PDF-', но первые 4 символа те же
        if not file_data[:4].startswith(b'%PDF'):
            logger_email.info(
                f'Вложение {filename} не является PDF (неверная сигнатура)'
            )
            return False

        logger_email.debug(f'Вложение {filename} прошло проверку.')
        return True

    def _ensure_unique_filename(self, filename: str, directory: Path) -> str:
        """Проверяет, существует ли файл с заданным именем в директории.

        Если файл существует, генерирует новое имя с временным штампом
        в формате "Программа_проверок_{дата и время с секундами}.pdf".
        Возвращает уникальное имя файла.
        """
        file_path = directory / filename
        if not file_path.exists():
            return filename

        base_name, ext = os.path.splitext(filename)
        base_name_clean = base_name.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{base_name_clean}_{timestamp}{ext}"
        logger_email.info(
            f'Файл {filename} уже существует, переименовываем в {new_filename}'
        )
        return new_filename

    def _process_attachment(self, attachment: Any, files_count: int) -> int:
        """Обрабатывает одно вложение, сохраняет если подходит.

        Возвращает обновленное количество сохраненных файлов.
        """
        logger_email.info(f'Вложение: {attachment.filename}')

        if (attachment.filename is None
                or attachment.filename != ATTACHMENT_FILENAME):
            logger_email.info(
                LOG_MSG_SKIP_ATTACHMENT.format(filename=attachment.filename))
            return files_count

        file_data = attachment.content
        if not self._validate_attachment(file_data, attachment.filename):
            logger_email.info(
                f'Вложение {attachment.filename} не прошло проверку'
            )
            return files_count

        unique_filename = self._ensure_unique_filename(
            attachment.filename, ATTACHMENTS_DIR
        )
        file_path = ATTACHMENTS_DIR / unique_filename
        try:
            with open(file_path, 'wb') as f:
                f.write(file_data)
            files_count += 1
            logger_email.info(f'Сохранено вложение: {unique_filename}')
        except OSError as e:
            logger_email.error(
                f'Ошибка сохранения файла {unique_filename}: {e}')
        return files_count

    def _process_message(self, message: Any, imap: Any) -> int:
        """Обрабатывает одно письмо, сохраняет подходящие вложения.

        Возвращает количество сохраненных вложений из этого письма.
        """
        sender = message.from_[0].email if message.from_ else SENDER_UNKNOWN
        if (message.subject == MESSAGE_SUBJECT
                and sender == SENDER_EMAIL):
            logger_email.info(LOG_MSG_EMAIL_SUITABLE)
            files_count = 0
            for attachment in message.attachments:
                files_count = self._process_attachment(attachment, files_count)
            return files_count
        return 0

    def read_email(self) -> Dict[str, str]:
        """Читает непрочитанные письма и сохраняет подходящие вложения."""
        logger_email.info(LOG_MSG_EMAIL_READ)
        try:
            with self.imap_client as imap:
                imap.select(IMAP_INBOX, readonly=False)
                uids = imap.search(IMAP_SEARCH_UNSEEN)
                if not uids:
                    logger_email.info(LOG_MSG_NEW_MAIL_NOT_FOUND)
                    return {
                        'status': STATUS_EMPTY,
                        'programm_files': INITIAL_FILES_COUNT
                    }
                logger_email.info(f'Найдено писем: {len(uids)}')
                ATTACHMENTS_DIR.mkdir(exist_ok=True)
                total_files = INITIAL_FILES_COUNT
                for uid in uids:
                    try:
                        message = imap.fetch(uid)
                        saved = self._process_message(message, imap)
                        total_files += saved
                        imap.mark_seen(message.uid)
                    except Exception as e:
                        logger_email.error(
                            f'Ошибка обработки письма UID {uid}: {e}',
                            exc_info=True
                        )
                        # Продолжаем обработку остальных писем
                logger_email.info(f'Сохранено вложений: {total_files}')
                return {'status': STATUS_OK, 'programm_files': total_files}
        except Exception as e:
            logger_email.error(f'Ошибка при работе с IMAP: {e}', exc_info=True)
            return {
                'status': STATUS_ERROR,
                'programm_files': INITIAL_FILES_COUNT
            }


email_client = EmailKndClient()
"""Глобальный экземпляр клиента для работы с электронной почтой.

Используется другими модулями для отправки и чтения писем.
"""
