# docker-ltnet
Provides pre-configured instances of the following that work together to help provide a snappier and safer network.

`unbound` for DNS caching and blackholing

`pixelserv` for serving up a 1x1 GIF to any request that has been black-holed in Unbound

`dnscrypt` for DNS encryption using supported DNSCrypt hosts specified in the dnscrypt-resolvers CSV (see below).

`squid` for HTTP caching

 All of these images are based on Alpine Linux to keep image size minimal.

### Unbound
Unbound has been configured to cache DNS requests and then forward them on to DNSCrypt.

`BLACKLIST_URL`: You can use any list provided at https://github.com/StevenBlack/hosts, and it will format the file for Unbound at container build time. To update the list, or use another, you can simply re-build this image.

unbound listens on 0.0.0.0:53 and forwards requests to 0.0.0.0:5353 (DNSCrypt), and 

### DNSCrypt
DNSCrypt has three options that can be configured from the docker-compose.yml file:
- `RESOLVERS_CSV_URL`: Defaults to the up-to-date CSV maintained at https://github.com/jedisct1/dnscrypt-proxy/raw/master/dnscrypt-resolvers.csv
- `DNSCRYPT_RESOLVER`: The name of the resolver from the dnscrypt-resolvers.csv
- `DNSCRYPT_LOCAL_ADDR`: Address and port to run DNSCrypt on. Defaults to 0.0.0.0:5353. *(If this is updated, you also need to update the Unbound config.)*

### Pixelserv
Pixelserv is a Python re-implementation of http://proxytunnel.sourceforge.net/files/pixelserv-inetd.pl.txt that supports HTTPS.  Unbound is configured to redirect any blacklisted hosts to Pixelserv for an instant response.

### Squid
Squid is configured as a forward proxy and listens on 0.0.0.0:3128, so once it's up, simply point your clients there to start caching content served over HTTP.

## Getting Started
`docker-compose build`

`docker-compose up -d`

Then point your clients to use the Unbound DNS and Squid HTTP forward proxy
