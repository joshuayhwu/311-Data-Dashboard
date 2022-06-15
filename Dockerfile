FROM python:3.7-slim-buster

EXPOSE 5500

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# SET THE DASHBOARDS TO PRELOAD
ENV PRELOAD=True

# Run the python Script
CMD ["python", "app.py"]