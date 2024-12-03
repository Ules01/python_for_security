# Use a lightweight Python base image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    iputils-ping net-tools && \
    pip install --no-cache-dir flask requests

# Set working directory
WORKDIR /app

# Copy application code into container
COPY . /app

# Ensure logs directory exists
RUN mkdir -p logs

# Make the startup script executable
RUN chmod +x start_honeypots.sh

# Expose ports for the honeypots
EXPOSE 80 22 8080

# Start honeypots
CMD ["./start_honeypots.sh"]
