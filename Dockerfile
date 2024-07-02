FROM python:3.9-alpine3.14

# Set the working directory inside the container
WORKDIR /home/user/web

# Set environment variables to avoid buffering and pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /home/user/web/requirements.txt
# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

# Copy the rest of your Django application code
COPY . .

