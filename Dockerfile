# Use the lightweight Python 11 Alpine image
FROM python:11-alpine

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apk update && \
    apk add --no-cache \
    bash \
    python3-dev \
    gcc \
    libc-dev \
    libffi-dev \
    musl-dev \
    openssl-dev \
    libxml2-dev \
    libxslt-dev \
    linux-headers && \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    pip install --upgrade markdown

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Ensure the entrypoint script is executable
COPY ./entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Use bash to run the entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
