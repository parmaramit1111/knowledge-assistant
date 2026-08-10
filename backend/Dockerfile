FROM python:3.12-slim-bookworm

# Prevent Python from writing .pyc files
# and ensure logs are immediately visible
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade OS packages to pick up latest security patches
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first
# so Docker can cache this layer
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Copy database migration configuration
COPY migrations ./migrations
COPY alembic.ini .

# Create local storage directory
RUN mkdir -p storage

# Application port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]