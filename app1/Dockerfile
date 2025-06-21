# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY ../requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY app1/ .

# Открываем порт, на котором будет работать приложение
EXPOSE 5001

# Команда для запуска приложения
CMD ["python", "app1.py"]