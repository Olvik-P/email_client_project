# Email Client Project

Проект для автоматизированной работы с электронной почтой с использованием пакета **MailToolsBox**: отправка тестовых писем и чтение входящих с сохранением определённых PDF-вложений.

## Функциональность

- **Отправка тестового письма** – отправляет письмо с заданными темой и телом на указанный адрес.
- **Чтение непрочитанных писем** – подключается к IMAP-серверу, ищет непрочитанные письма.
- **Фильтрация писем** – отбирает письма с определённым отправителем и темой.
- **Валидация и сохранение вложений** – проверяет, что вложение является PDF-файлом, не превышает 10 МБ, и сохраняет его в папку `Programms/` с уникальным именем (если файл уже существует).
- **Структурированное логирование** – использует кастомный логгер на основе `loguru` с выводом в консоль (в режиме разработки) и в файл (в продакшене).

## Структура проекта

```
email_client_project/
├── email_knd/                    # Основной модуль работы с почтой
│   ├── __init__.py
│   └── core/
│       ├── __init__.py
│       ├── config.py             # Класс EmailKndClient и глобальный экземпляр email_client
│       └── constants.py          # Константы (адреса, пути, сообщения)
├── logger_costom/                # Кастомный логгер
│   ├── __init__.py               # Инициализация логгера logger_email
│   ├── constants.py              # Константы форматирования и уровней логирования
│   └── costom_loguru.py          # Класс LoggerLoguru
├── test.py                       # Основной скрипт для запуска
├── .env.example                  # Пример файла переменных окружения
├── requirements.txt              # Зависимости Python
├── ruff.toml                     # Конфигурация линтера Ruff
├── logs/                         # Папка для лог-файлов (создаётся автоматически)
├── Programms/                    # Папка для сохранённых PDF-вложений (создаётся автоматически)
└── README.md                     # Этот файл
```

## Требования и установка

1. **Python 3.8+**
2. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка окружения

1. Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

2. Отредактируйте `.env`, указав реальные данные вашего почтового ящика:

```env
ENV_TYPE=dev                     # dev – режим разработки, prod – продакшен

EMAIL=example@example.com
EMAIL_PASSWORD=your_email_password_here
SMTP_SERVER=smtp.example.com
SMTP_PORT=465
EMAIL_SECURITY=ssl

IMAP_EMAIL=example@example.com
IMAP_PASSWORD=your_imap_password_here
IMAP_SERVER=imap.example.com
IMAP_PORT=993
IMAP_SECURITY=ssl
```

**Важно:** Для работы с IMAP необходимо разрешить доступ по паролю приложений (если используется Gmail) или настроить соответствующие параметры безопасности.

## Использование

Запустите основной скрипт:

```bash
python test.py
```

Скрипт выполнит следующие действия:

1. Проверит наличие обязательных переменных окружения.
2. Отправит тестовое письмо на адрес, указанный в `RECIPIENT_EMAIL` (по умолчанию `example_recipient@example.com`).
3. Подключится к IMAP-серверу и прочитает все непрочитанные письма.
4. Для каждого письма, у которого отправитель `example_sender@example.com` и тема `Программа проверок`, проверит вложение `Программа проверок.pdf`.
5. Если вложение прошло валидацию (PDF, ≤10 МБ), сохранит его в папку `Programms/`. Если файл с таким именем уже существует, добавит временную метку.
6. Выведет результаты в лог.

## Логирование

Проект использует кастомный логгер `logger_email` из модуля `logger_costom`.

- **В режиме разработки (`ENV_TYPE=dev`)** – логи выводятся только в консоль с уровнем `DEBUG`.
- **В продакшене (`ENV_TYPE=prod`)** – логи выводятся в консоль (если `LOG_USE_CONSOLE=True`) и в файл `logs/log_email.log` с уровнем `INFO`, ротацией 10 МБ и retention 7 дней.

Пример лога:

```
INFO      2026-04-26 11:10:00 username=SYSTEM user_id=0  Начало работы ...
DEBUG     2026-04-26 11:10:00 username=SYSTEM user_id=0  Проверка переменные окружения ...
INFO      2026-04-26 11:10:00 username=SYSTEM user_id=0  Настраиваем отправку емаил ...
```

Логгер автоматически добавляет поля `username` и `user_id` (по умолчанию `SYSTEM` и `0`). При вызове методов логирования можно передать эти параметры:

```python
from logger_costom import logger_email

logger_email.info("Сообщение", username="john", user_id=42)
```

## Зависимости

Основные зависимости перечислены в `requirements.txt`:

- **MailToolsBox** – для работы с SMTP/IMAP
- **loguru** – для структурированного логирования
- **python-dotenv** – для загрузки переменных окружения
- **ruff** – линтинг и форматирование

Полный список см. в `requirements.txt`.

## Docker

Проект может быть запущен в Docker-контейнере. Для этого в корне проекта создан `Dockerfile`.

### Сборка образа

```bash
docker build -t email-client:latest .
```

### Запуск контейнера

Для запуска необходимо передать переменные окружения. Можно использовать файл `.env`:

```bash
docker run --rm --env-file .env email-client:latest
```

Или передать переменные напрямую:

```bash
docker run --rm \
  -e ENV_TYPE=prod \
  -e EMAIL=your_email@example.com \
  -e EMAIL_PASSWORD=your_password \
  -e SMTP_SERVER=smtp.example.com \
  -e SMTP_PORT=465 \
  -e EMAIL_SECURITY=ssl \
  -e IMAP_EMAIL=your_email@example.com \
  -e IMAP_PASSWORD=your_password \
  -e IMAP_SERVER=imap.example.com \
  -e IMAP_PORT=993 \
  -e IMAP_SECURITY=ssl \
  email-client:latest
```

### Постоянные данные

Контейнер создает директории `logs/` и `Programms/` внутри контейнера. Чтобы сохранить данные на хосте, можно смонтировать volumes:

```bash
docker run --rm \
  --env-file .env \
  -v ./logs:/app/logs \
  -v ./Programms:/app/Programms \
  email-client:latest
```

### Тегирование и публикация

Для публикации образа в реестре (например, Docker Hub):

```bash
docker tag email-client:latest yourusername/email-client:latest
docker push yourusername/email-client:latest
```

## Лицензия
- Разработано: Олег Пономарев
- Контакты: olpon00@mail.ru
- Лицензия: MIT