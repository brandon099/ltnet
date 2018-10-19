# build stage
FROM golang:alpine AS build-env
WORKDIR /go/src/app
RUN apk update && apk upgrade && \
    apk add --no-cache git
RUN git clone https://github.com/bmrzycki/nullserv.git && \
    cd nullserv && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -a -installsuffix cgo -ldflags="-w -s" -o nullserv

# final stage
FROM scratch
COPY --from=build-env /go/src/app/nullserv/nullserv /
ENTRYPOINT ["/nullserv"]
