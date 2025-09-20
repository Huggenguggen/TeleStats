# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY telegram_analyzer/ ./telegram_analyzer/

# Create directories for uploads and DB
RUN mkdir -p /app/telegram_analyzer/uploads
RUN touch /app/telegram_analyzer/telegram.db

# Expose port
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=telegram_analyzer/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run the app
CMD ["flask", "run"]
