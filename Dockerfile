# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для сборки пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем необходимые директории
RUN mkdir -p logs Programms

# Устанавливаем переменные окружения по умолчанию
ENV ENV_TYPE=prod \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Точка входа - запуск основного скрипта
ENTRYPOINT ["python", "test.py"]