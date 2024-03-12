# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app/bot

# Install dependencies
COPY requirements.txt /app/bot/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/bot/