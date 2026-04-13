# Використовуємо офіційний образ Python
FROM python:3.12-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо системні залежності для psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проекту
COPY . .

# Команда для запуску (використовуємо 0.0.0.0, щоб Docker міг прокинути порт)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]