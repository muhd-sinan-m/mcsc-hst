# Use official lightweight Python 3.11 base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Create required directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Ensure entrypoint script has execution permissions and Unix LF line endings
RUN chmod +x /app/entrypoint.sh \
    && sed -i 's/\r$//' /app/entrypoint.sh

# Expose container port
EXPOSE 8000

# Set entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default startup command running Gunicorn WSGI server
CMD ["gunicorn", "mcsc.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
