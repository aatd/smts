FROM balenalib/raspberry-pi-debian-python:latest

WORKDIR /mythief-be

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /mythief-be/requirements.txt

RUN pip install -r /mythief-be/requirements.txt

COPY . /mythief-be

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "src/main.py" ]