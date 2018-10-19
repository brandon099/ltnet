# build stage
FROM golang:alpine AS build-env
WORKDIR /go/src/app
RUN apk update && apk upgrade && \
    apk add --no-cache git
RUN git clone https://github.com/PierreZ/goStatic gostatic && \
    cd gostatic && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -a -installsuffix cgo -ldflags="-w -s" -o gostatic
WORKDIR /
RUN git clone https://github.com/looterz/reaper

# final stage
FROM scratch
ADD https://curl.haxx.se/ca/cacert.pem /etc/ssl/certs/ca-certificates.crt
COPY --from=build-env /reaper /srv/http
COPY --from=build-env /go/src/app/gostatic/gostatic /
COPY ./config.js /srv/http/js/config.js

ENTRYPOINT ["/gostatic"]
CMD ["-port", "8081"]
