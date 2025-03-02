# Use the official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the local folder to the container
COPY . .

# Install required dependencies
RUN pip install -r requirements.txt

# Command to run your script
CMD ["python", "Fetch Historical Data.py"]
