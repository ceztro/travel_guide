# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install psycopg2 and boto3 for PostgreSQL and AWS Secrets Manager access
RUN pip install --no-cache-dir psycopg2-binary boto3

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variable for Flask app name
ENV NAME TravelGuidanceApp

# Run app.py when the container launches
CMD ["python", "app.py"]