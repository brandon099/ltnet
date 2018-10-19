# docker-ltnet
Provides pre-configured instances of the following that work together to help provide a snappier and safer network.

`grimd` for DNS caching and blackholing. Also forwards good requests to `dnscrypt-proxy`.
https://github.com/looterz/grimd


`reaper` for showing statistics on DNS queries to `grimd`.
https://github.com/looterz/reaper


`nullserv` for serving up the smallest valid response to most requests that have been black-holed in grimd, including HTTPS.
https://github.com/bmrzycki/nullserv


`dnscrypt-proxy` for DNS over TLS.
https://github.com/jedisct1/dnscrypt-proxy


All of these images utilize multi-stage docker builds. The first step uses `golang:alpine`,
and the final step utilizes Docker's built-in [scratch](https://docs.docker.com/samples/library/scratch/).

You can safely remove the build specific images to save some space. The final size on disk for all four images combined is under 35MB.

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
Listens on 0.0.0.0:8081. Edit `reaper/config.js` API URI setting to point to where your Grimd API is running.
 
## Getting Started
`docker-compose build`

`docker-compose up -d`

Then point your clients to use Grimd as it's resolver
