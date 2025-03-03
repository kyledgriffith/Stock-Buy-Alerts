# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Flask
ENV PORT=8080

# Expose the port that Flask runs on
EXPOSE 8080

# Run both the fetch script and Flask API
CMD ["sh", "-c", "python fetch_historical_data.py & python app.py"]