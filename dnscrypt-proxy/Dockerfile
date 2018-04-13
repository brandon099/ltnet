FROM alpine:latest

ARG RESOLVERS_CSV_URL

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --update --no-cache dnscrypt-proxy ca-certificates && update-ca-certificates

CMD /usr/bin/dnscrypt-proxy --config /etc/dnscrypt-proxy/dnscrypt-proxy.toml
