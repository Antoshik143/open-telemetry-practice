# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY ../requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY app2/ .

# Открываем порт, на котором будет работать приложение
EXPOSE 5002

# Команда для запуска приложения
CMD ["python", "app2.py"]