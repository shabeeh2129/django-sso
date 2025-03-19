FROM python:3.10-slim

WORKDIR /app

# Install system dependencies as root
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Start the application
CMD ["gunicorn", "sso_system.wsgi:application", "--bind", "0.0.0.0:8000"]
