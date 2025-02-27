
FROM python:3.9-slim AS flask

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Step 2: Use Nginx as the base image
FROM nginx:latest

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Install Python and Flask dependencies inside the Nginx container
RUN apt update && apt install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=flask /app /app
RUN pip3 install -r requirements.txt

# Expose ports for Nginx
EXPOSE 80

# Start both Nginx and Flask
CMD service nginx start && python3 app.py
