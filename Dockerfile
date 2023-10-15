# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy everythin into the container
COPY * ./
COPY utils/* ./utils/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Run your Python script
CMD ["python", "watcher.py"]
