# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Create the directory for the SQLite database
RUN mkdir -p /app/instance

# Expose the port used by the Entities Service
EXPOSE 5001

# Set the command to run the application
CMD ["python3", "main.py"]
