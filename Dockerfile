# Використовуємо офіційний образ Python як базовий
FROM python:3.12.2

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли скрипту та Pipfile в робочу директорію контейнера
COPY assistant.py Pipfile* /app/

# Встановлюємо Pipenv
RUN pip install pipenv

# Встановлюємо залежності з Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Вказуємо команду для запуску застосунку
CMD ["pipenv", "run", "python", "assistant.py"]

