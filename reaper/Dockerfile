# build stage
FROM alpine AS build-env

ARG GRIMD_API_URL

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --update --no-cache bash git openssh
RUN git clone https://github.com/looterz/reaper
RUN sed -i -e "s/localhost:8080/$GRIMD_API_URL/g" reaper/js/index.js

# final stage
FROM alpine
WORKDIR /var/www/html
RUN apk add --update --no-cache caddy tini
COPY ./Caddyfile /etc/Caddyfile
COPY --from=build-env /reaper /var/www/html
ENTRYPOINT ["/sbin/tini"]
CMD ["caddy", "-quic", "--conf", "/etc/Caddyfile"]
