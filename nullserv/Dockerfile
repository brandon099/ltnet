# build stage
FROM golang:alpine AS build-env
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh
RUN git clone https://github.com/bmrzycki/nullserv.git
RUN cd nullserv && go build

# final stage
FROM alpine
WORKDIR /app
COPY --from=build-env /go/nullserv/nullserv /app/
ENTRYPOINT /app/nullserv
