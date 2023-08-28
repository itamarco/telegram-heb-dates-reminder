FROM python:3.9-slim-buster

# dependencies for psycog2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

WORKDIR /app

COPY ./app /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 80

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]