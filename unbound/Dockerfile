FROM python:3-alpine

USER root

ARG BLACKLIST_URLS

RUN apk add --update --no-cache unbound ca-certificates wget
RUN update-ca-certificates

RUN mkdir /app
WORKDIR /app
COPY ./list-download.py .

RUN python list-download.py /etc/unbound/a-records.conf "$BLACKLIST_URLS"

ENTRYPOINT ["unbound"]
CMD ["-d"]
