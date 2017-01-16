FROM alpine:latest

ENV goaccess_version=1.1.1
ENV build_deps='go build-base ncurses-dev'

RUN set -x && \
        apk add --update --no-cache ncurses $build_deps && \
        wget -O /tmp/goaccess.tar.gz http://tar.goaccess.io/goaccess-$goaccess_version.tar.gz && \
        tar -xzvf /tmp/goaccess.tar.gz -C /tmp && \
        cd /tmp/goaccess-$goaccess_version && \
        ./configure --enable-utf8 && \
        make && \
        make install && \
        apk del $build_deps && \
        rm -rf /tmp/goaccess*

ADD ./goaccess.conf /usr/local/etc/goaccess.conf

EXPOSE 7890

ENTRYPOINT ["/usr/bin/goaccess"]
CMD ["--real-time-html"]
# TODO: Link the access-log from pixelsrv to this container through a volume
#       Fix IndexError: list index out of range at File "/pixelsrv.py", line 35, in parse_request
# goaccess -f ../pixelsrv/access.log -p ./goaccess.conf -o ./report.html --real-time-html
