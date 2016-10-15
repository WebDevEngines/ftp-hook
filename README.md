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
	"form_paramter": ""
}
```

### Deploy 

https://hub.docker.com/r/webdevenginesllc/ftp-hook/

### Build the docker image  
```
docker build -t ftp_hook .
```

### Run the docker image  
```
docker run \
  -it \
  -p 0.0.0.0:21:21 \
  -p 0.0.0.0:20:20 \
  -p 0.0.0.0:5000-5010:5000-5010 \
  -e AUTHENTICATION_URL='https://localhost/auth/' \
  ftp_hook
```

### Contributors
- https://github.com/n4ym  
- https://github.com/nickcrafford
