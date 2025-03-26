# Используем официальный Python-образ
FROM python:3.9

WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запуск сервера
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
