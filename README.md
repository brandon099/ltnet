# docker-ltnet
Provides pre-configured instances of the following that work together to help provide a snappier and safer network.

`grimd` for DNS caching and blackholing
https://github.com/looterz/grimd


`reaper` for showing statistics on DNS queries to `grimd`
https://github.com/looterz/reaper


`nullserv` for serving up a 1x1 GIF to any request that has been black-holed in grimd
https://github.com/bmrzycki/nullserv


`dnscrypt-proxy` for DNS over TLS.
https://github.com/jedisct1/dnscrypt-proxy


All of these images are based on Alpine Linux to keep image size minimal.

The `grimd` and `nullserve` Dockerfile's use multi-stage builds to keep the final image small.

You can safely remove the build specific images and save some space.

### grimd
Grimd has been configured to cache DNS requests, blackhole blacklisted requests, and forward good requests on to DNSCrypt-proxy.

grimd listens on 0.0.0.0:53 for DNS and 0.0.0.0:8080 for API (used by `reaper` to show stats and perform light controls)

_You must edit the NULLSERV_IP arg value in the docker-compose.yml file to ensure your nullroute is set to the correct IP._

### dnscrypt-proxy
dnscrypt-proxy has a config file you can use to customize its settings.

dnscrypt-proxy listens on 0.0.0.0:5353 by default.

### nullserv
grimd is configured to redirect any blacklisted hosts to nullserv for an instant response (HTTP + HTTPS).

nullserv listens on 0.0.0.0:80 and 0.0.0.0:443 by default.

### reaper
_You must edit the GRIMD_API_URL arg value in the docker-compose.yml for reaper._

Default listens on 0.0.0.0:8081. Update the Caddyfile if you want it to be available on another port.

## Getting Started
`docker-compose build`

`docker-compose up -d`

Then point your clients to use Grimd as it's resolver
