FROM golang:alpine

RUN apk add --update --no-cache git
RUN go get github.com/shadowsocks/shadowsocks-go/cmd/shadowsocks-server

EXPOSE 8388

ENTRYPOINT ["/go/bin/shadowsocks-server"]
