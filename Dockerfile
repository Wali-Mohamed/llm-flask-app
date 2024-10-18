# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file to install dependencies
COPY requirements.txt . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . /app

# Expose the Flask port
EXPOSE 5000

# Command to run the app
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "local_app:app"]
#CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["python", "local_app.py"]
# Command to run the shell script (start.sh)
CMD ["sh", "./start.sh"]

