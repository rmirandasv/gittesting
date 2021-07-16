# image
FROM scratch
ADD ubuntu-focal-oci-amd64-root.tar.gz /
RUN apt -y install python3 git
ENV DOCKER_HOME=/home/app/webapp

RUN mkdir -p $DOCKER_HOME

WORKDIR $DOCKER_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m venv vendor
RUN source vendor/bin/activate
RUN python3 -m pip install --upgrade pip

COPY . $DOCKER_HOME

RUN git pull
RUN git checkout ronald-patch1
RUN git checkout master-fix
RUN git checkout master
RUN git checkout develop

RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

CMD python3 fstest/manage.py runserver 0.0.0.0:8000
