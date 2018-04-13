# docker-ltnet
Provides pre-configured instances of the following that work together to help provide a snappier and safer network.

`grimd` for DNS caching and blackholing
https://github.com/looterz/grimd

`reaper` for showing statistics on DNS queries to `grimd`
https://github.com/looterz/reaper

`nullserv` for serving up a 1x1 GIF to any request that has been black-holed in Unbound
https://github.com/bmrzycki/nullserv

`dnscrypt-proxy` for DNS over TLS.
https://github.com/jedisct1/dnscrypt-proxy

All of these images are based on Alpine Linux to keep image size minimal. The `grimd` and `nullserve` Dockerfile's use multi-stage builds to keep the final image small. You can safely remove the build specific images and save some space.

### grimd
Grimd has been configured to cache DNS requests, blackhole blacklisted requests, and forward good requests on to DNSCrypt-proxy.
grimd listens on 0.0.0.0:53 for DNS and 0.0.0.0:8080 for API (used by `reaper` to show stats and perform light controls)
You must edit the NULLSERV_IP arg in the docker-compose.yml file to ensure your nullroute is set to the properly nullroute blackisted requests.

### dnscrypt-proxy
dnscrypt-proxy has a config file you can use to customize its settings.
dnscrypt-proxy listens on 0.0.0.0:5353 (DNSCrypt-proxy)

### nullserv
nullserv is a Golang re-implementation of http://proxytunnel.sourceforge.net/files/pixelserv-inetd.pl.txt that supports HTTPS, and many file types to speed your network up.
grimd is configured to redirect any blacklisted hosts to nullserv for an instant response.
nullserv listens on 0.0.0.0:80 and 0.0.0.0:443

### reaper
You must edit the GRIMD_API_URL in the docker-compose.yml for reaper -- this tells the UI where the grimd API is at so it can pull the data, and since it is client side, it must be an address your computer has access to.
Default listens on 0.0.0.0:8081. Update the Caddyfile if you want it to be available on another port.

## Getting Started
`docker-compose build`

`docker-compose up -d`

Then point your clients to use Grimd as it's resolver
