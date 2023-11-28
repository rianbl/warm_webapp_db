# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY app/requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the SQL script and the rest of the application code
COPY init.sql .
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

# Install gosu
RUN apt-get update && apt-get install -y gosu

# Start PostgreSQL and run the SQL script
# CMD ["sh", "-c", "service postgresql start && gosu postgres psql -h mypsql -U postgres -f init.sql && service postgresql stop"]

# Command to run the application
CMD ["python", "./app/app.py"]
