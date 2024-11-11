# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install MySQL client to connect with the database (since you're using MySQL in your database.py)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /app/wait-for-it.sh

# Make the wait-for-it.sh script executable
RUN chmod +x /app/wait-for-it.sh

# Expose the port the app will run on
EXPOSE 8000

# Run the FastAPI app with uvicorn using wait-for-it.sh to ensure DB is ready
CMD ["/app/wait-for-it.sh", "db:3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
