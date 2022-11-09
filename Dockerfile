FROM python:3.8.9
# Run commands from / directory inside container
WORKDIR /
# Copy requirements from local to docker image
COPY requirements.txt /
# Install the dependencies in the docker image
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy everything from the current dir to the image
COPY . .
