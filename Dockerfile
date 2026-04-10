FROM python:3.10-slim

# Install system dependencies (for pytesseract, mysql client)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables
ENV PORT=5000
ENV FLASK_DEBUG=0

EXPOSE 5000

# Start server
CMD gunicorn -w 4 -b 0.0.0.0:$PORT app:app
