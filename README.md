# Quick Start

### Build the docker image  
```
docker build -t ftp_hook .
```

### Run the docker image  
```
docker run \
  -it -p 0.0.0.0:21:21 \
  -e WEB_HOOK='https://localhost/upload/' \
  -e FTP_USERNAME='test' \
  -e FTP_PASSWORD='test' \
  -e WEB_HOOK_FORM_PARAMETER='file' \
  ftp_hook
```
