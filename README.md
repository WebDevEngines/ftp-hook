# Quick Start

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
  -e WEB_HOOK='https://localhost/upload/' \
  -e FTP_USERNAME='test' \
  -e FTP_PASSWORD='test' \
  -e WEB_HOOK_FORM_PARAMETER='file' \
  ftp_hook
```
