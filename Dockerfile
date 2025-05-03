# Use a Python base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY app.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask requests

# Expose port
EXPOSE 80

# Run the app
CMD ["python", "app.py"]
