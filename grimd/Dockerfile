# build stage
FROM golang:alpine AS build-env
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh
RUN git clone https://github.com/looterz/grimd.git
RUN cd grimd && go get -d -v && go build

# final stage
FROM alpine

ARG NULLSERV_IP

WORKDIR /app
RUN apk add --no-cache ca-certificates && update-ca-certificates
COPY --from=build-env /go/grimd/grimd /app/
COPY ./grimd.toml /etc/grimd.toml
RUN sed -i -e "s/nullroute = \"0.0.0.0\"/nullroute = \"$NULLSERV_IP\"/g" /etc/grimd.toml

ENTRYPOINT /app/grimd -update -config /etc/grimd.toml
