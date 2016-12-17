FROM alpine:latest

ARG BLACKLIST_URL

RUN apk add --update --no-cache unbound ca-certificates wget
RUN update-ca-certificates
RUN wget "$BLACKLIST_URL" -O /tmp/blacklist-hosts
RUN cat /tmp/blacklist-hosts | grep '^0\.0\.0\.0' | awk '{print "local-zone: \""$2"\" redirect\nlocal-data: \""$2" A 0.0.0.0\""}' > /etc/unbound/a-records.conf
RUN rm /tmp/blacklist-hosts

ENTRYPOINT ["unbound"]
CMD ["-d"]
