# Copyright (c) 2016 WebDevEngines LLC.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM ubuntu:14.04
MAINTAINER WebDevEngines LLC <n.crafford@webdevengines.com>
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d
RUN sudo apt-get update && sudo apt-get install -y build-essential libffi-dev libssl-dev python-dev python python-pip openssl
RUN sudo pip install pyftpdlib
RUN sudo pip install pyopenssl
USER root
RUN chmod 777 /opt/ 
ADD . /opt/
RUN chmod -R 777 /opt/ 
RUN cd /opt/ && sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ftps.key -out ftps.crt -subj "/C=US/ST=CA/L=LG/O=Dis/CN=webdevengines.com" && cat ftps.crt ftps.key > ftps.pem
RUN mkdir /jail/
RUN sudo ln -s /opt/run.sh /bin/run_ftp
CMD run_ftp
EXPOSE 20 21 50000-50010