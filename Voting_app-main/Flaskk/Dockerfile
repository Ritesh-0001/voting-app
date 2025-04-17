# Use an official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose the Flask app port
EXPOSE 5001

# Run the Flask app
CMD ["python", "app.py"]
