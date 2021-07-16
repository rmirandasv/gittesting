# image
FROM python:3.8.10

ENV DOCKER_HOME=/home/app/webapp

RUN mkdir -p $DOCKER_HOME

WORKDIR $DOCKER_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

COPY . $DOCKER_HOME

RUN python -m pip install -r requirements.txt

EXPOSE 8000

CMD python fstest/manage.py runserver 0.0.0.0:8000
