# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Run the command to start the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
