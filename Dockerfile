# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Expose the port on which your Django application will run (usually 8000)
EXPOSE 8000

# Run the command to start your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

