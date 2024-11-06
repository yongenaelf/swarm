# Use a base image with Python 3.10+
FROM python:3.10-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set the working directory
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to run the chat_interface.py file
ENTRYPOINT ["panel", "serve", "chat_interface.py"]
