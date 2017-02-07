# Quick Start

### Create an authentication endpoint
e.g. `https://localhost/auth/`

Which accepts the POST parameters:
- `username`
- `password`

And returns on successful authentication:
```
{
	// URL to POST files PUT via FTP Hook
	"url": "",
	// Form parameter to use when POSTing files
	"form_parameter": ""
}
```

### Deploy 

https://hub.docker.com/r/webdevenginesllc/ftp-hook/

### Build the docker image  
```
docker build -t ftp_hook .
```

### Run the docker image  

Pass `ENABLE_FTPS` variable to use self-signed SSL cert (Generated during docker image build).

```
docker run \
  -it \
  -p 0.0.0.0:21:21 \
  -p 0.0.0.0:20:20 \
  -p 0.0.0.0:5000-5100:5000-5100 \
  -e AUTHENTICATION_URL="https://localhost/auth/" \
  -e ENABLE_FTPS="True"
  -e DOMAIN="yourhost.com"
  ftp_hook
```

### Contributors
- https://github.com/n4ym  
- https://github.com/nickcrafford
