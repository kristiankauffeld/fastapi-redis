# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9.18
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the source code into the container.
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt