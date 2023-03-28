# base image
FROM python:3.9.7-buster

# options
ENV PYTHONUNBUFFERED 1

# Set working directory
RUN mkdir secure_home
# set the working directory
COPY . /secure_home/
# coppy commands
WORKDIR /secure_home

# update docker-iamage packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

# update pip
RUN pip install --upgrade pip
# install psycopg for connect to pgsql
RUN pip install psycopg2-binary
# install python packages
RUN pip install -r requirements.txt
# create static directory
RUN mkdir static
# RUN python manage.py collectstatic --no-input
EXPOSE 5000
CMD ["gunicorn","--bind", ":5000", "secure_home.wsgi:application"]