FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .
ENV PYTHONPATH=/app


# Make wait script executable
RUN chmod +x wait-for-postgres.sh

# Expose port
EXPOSE 5000

# Default command (can be overridden by docker-compose)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
