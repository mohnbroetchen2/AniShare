# pull the official base image
FROM python:3.6

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
#RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]