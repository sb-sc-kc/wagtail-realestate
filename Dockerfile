# Use an official Python runtime as a parent image
FROM python:3.8
LABEL maintainer="hello@wagtail.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1

# Install libenchant and create the requirements folder.
RUN apt-get update -y \
    && apt-get install -y libenchant-dev postgresql-client \
    && mkdir -p /code/requirements
RUN apt-get install vim less -y

# Install the bakerydemo project's dependencies into the image.
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /code/requirements.txt

# Install wagtail from the host. This folder will be overwritten by a volume mount during run time (so that code
# changes show up immediately), but it also needs to be copied into the image now so that wagtail can be pip install'd.
# COPY ./wagtail /code/wagtail/
# RUN cd /code/wagtail/ \
#     && pip install -e .[testing,docs]
