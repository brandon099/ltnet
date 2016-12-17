FROM alpine:latest

RUN apk add --update --no-cache squid
ADD ./squid.conf /etc/squid/squid.conf
RUN squid -z -F

ENTRYPOINT ["squid"]
CMD ["-N"]
