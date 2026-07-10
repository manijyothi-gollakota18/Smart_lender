# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Set work directory
WORKDIR /app

# Install system dependencies (required for some packages if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
RUN pip install --no-cache-dir gunicorn --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org

# Copy project files
COPY . /app/

# Generate plots and train model inside image to ensure artifacts are baked in
RUN python eda.py && python train_model.py

# Expose port
EXPOSE 5000

# Run Flask application using Gunicorn WSGI server
CMD gunicorn --bind 0.0.0.0:$PORT app:app
