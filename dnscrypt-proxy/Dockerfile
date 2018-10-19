# build stage
FROM golang:alpine AS build-env
WORKDIR /go/src/app
RUN apk update && apk upgrade && \
    apk add --no-cache git
RUN git clone https://github.com/jedisct1/dnscrypt-proxy && \
    cd dnscrypt-proxy/dnscrypt-proxy && go get -d -v && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -a -installsuffix cgo -ldflags="-w -s" -o dnscrypt-proxy

# final stage
FROM scratch
ADD https://curl.haxx.se/ca/cacert.pem /etc/ssl/certs/ca-certificates.crt
COPY --from=build-env /go/src/app/dnscrypt-proxy/dnscrypt-proxy/dnscrypt-proxy /
COPY ./dnscrypt-proxy.toml /dnscrypt-proxy.toml

ENTRYPOINT ["/dnscrypt-proxy"]
