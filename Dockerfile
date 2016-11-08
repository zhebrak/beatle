FROM alpine:3.4

MAINTAINER Alexander Zhebrak

RUN mkdir /beatle
WORKDIR /beatle

COPY *.py /beatle/
COPY requirements.txt /beatle/

RUN apk add --update python3 git py-pip

RUN python3 -m venv /beatle/.venv
RUN cd /beatle && /beatle/.venv/bin/pip install pip --upgrade && /beatle/.venv/bin/pip install -r requirements.txt

ENTRYPOINT ["/beatle/.venv/bin/python", "beatle.py"]
