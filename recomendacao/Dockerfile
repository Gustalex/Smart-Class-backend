FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir -p /app/data


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Runserver
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8004"]