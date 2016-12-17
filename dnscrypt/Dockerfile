FROM alpine:latest

ARG RESOLVERS_CSV_URL

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --update --no-cache dnscrypt-proxy ca-certificates wget
RUN update-ca-certificates
RUN wget "$RESOLVERS_CSV_URL" -O /usr/share/dnscrypt-proxy/dnscrypt-resolvers.csv

CMD /usr/sbin/dnscrypt-proxy --local-address=$DNSCRYPT_LOCAL_ADDR --resolver-name=$DNSCRYPT_RESOLVER
