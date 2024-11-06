# Use a base image with Python 3.10+
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the software_team example files into the Docker image
ARG EXAMPLES_DIR=examples/software_team
COPY ${EXAMPLES_DIR} /app
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to run the main.py file
ENTRYPOINT ["python", "main.py"]
