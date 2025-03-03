# Use an official Python runtime
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Run the script
CMD ["python", "fetch_historical_data.py"]