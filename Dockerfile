# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for Pillow and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libblas-dev \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for the Flask app
ENV FLASK_APP=mememaker.py

# Expose the port that the app will run on
EXPOSE 8080

# Run the application using Flask (in production, using app.run() with host='0.0.0.0')
CMD ["python", "mememaker.py"]
