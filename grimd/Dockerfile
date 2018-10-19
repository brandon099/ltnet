# build stage
FROM golang:alpine AS build-env
WORKDIR /go/src/app
RUN apk update && apk upgrade && \
    apk add --no-cache git gcc musl-dev
RUN git clone https://github.com/looterz/grimd.git && \
    cd grimd && go get -d -v && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -a -installsuffix cgo -ldflags="-w -s" -o grimd

# final stage
FROM scratch
ADD https://curl.haxx.se/ca/cacert.pem /etc/ssl/certs/ca-certificates.crt
COPY --from=build-env /go/src/app/grimd/grimd /
COPY ./grimd.toml /etc/grimd.toml

ENTRYPOINT ["/grimd"]
