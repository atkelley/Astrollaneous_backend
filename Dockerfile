FROM python:3.11-slim

# Install PostgreSQL development dependencies
RUN apt-get update && apt-get install -y libpq-dev build-essential && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run migrations and start app
CMD gunicorn api.wsgi:application --bind 0.0.0.0:$PORT

