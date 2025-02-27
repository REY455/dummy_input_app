FROM python:3.9-slim

# Install NGINX and Supervisor
RUN apt-get update && \
    apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy Flask app requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY . .

# Copy NGINX configuration and Supervisor config
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose necessary ports
EXPOSE 5000 80

# Start Supervisor
CMD ["/usr/bin/supervisord"]
