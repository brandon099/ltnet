# build stage
FROM golang:alpine AS build-env
WORKDIR /go/src/app
ARG GRIMD_API_URL
RUN apk update && apk upgrade && \
    apk add --no-cache git
RUN git clone https://github.com/PierreZ/goStatic gostatic && \
    cd gostatic && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -a -installsuffix cgo -ldflags="-w -s" -o gostatic
WORKDIR /
RUN git clone https://github.com/looterz/reaper
# TODO: Just copy the override config file supported by latest reaper
RUN sed -i -e "s/localhost:8080/$GRIMD_API_URL/g" reaper/js/index.js

# final stage
FROM scratch
ADD https://curl.haxx.se/ca/cacert.pem /etc/ssl/certs/ca-certificates.crt
COPY --from=build-env /reaper /srv/http
COPY --from=build-env /go/src/app/gostatic/gostatic /

ENTRYPOINT ["/gostatic"]
CMD ["-port", "8081"]
