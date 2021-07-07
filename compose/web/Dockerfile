# Use an official Python runtime as a parent image
FROM python:3.9
LABEL maintainer="hello@wagtail.io"

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install libenchant and create the requirements folder.
RUN apt-get update -y \
    && apt-get install -y libenchant-dev postgresql-client \
    && mkdir -p /app
RUN apt-get install -y vim less net-tools iputils-ping tcpdump
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Install the project's dependencies into the image.
COPY ./requirements-production.txt /microservice/requirements.txt
COPY ./init.db.sh /docker-entrypoint-initdb.d/init.sh
COPY ./gunicorn.conf.py /microservice/gunicorn.conf.py
COPY ./test-db.yaml /microservice/test-db.yaml
COPY ./app-start.sh /microservice/app-start.sh
# COPY ./mysite /microservice/app

WORKDIR /microservice

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# RUN python app/manage.py migrate
# RUN python app/manage.py loaddata --format yaml test-db.yaml

EXPOSE 8000

# ENTRYPOINT ["python", "app/manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", ":8000", "mysite.wsgi"]
