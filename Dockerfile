# pull the official base image
FROM python:3.6


RUN mkdir /anishare

# set work directory
WORKDIR /anishare

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#RUN pip install --upgrade pip 
#COPY ./requirements.txt /usr/src/app
#RUN pip install -r requirements.txt

# copy project
ADD . /anishare/

RUN apt-get update
RUN apt-get dist-upgrade
RUN apt-get -y install git python3-dev python3-ldap python3-pip default-libmysqlclient-dev default-mysql-client ldap-utils libldap2-dev libsasl2-dev

RUN pip install -r requirements.txt
#EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]