# Copyright (c) 2016 WebDevEngines LLC.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM ubuntu:16.04
MAINTAINER WebDevEngines LLC <n.crafford@webdevengines.com>
USER root
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d
RUN apt-get update && apt-get install -y build-essential libffi-dev libssl-dev python-dev python python-pip openssl sudo
RUN pip install pyftpdlib
RUN pip install pyopenssl
RUN pip install requests
RUN chmod 777 /opt/ 
ADD . /opt/
RUN chmod -R 777 /opt/ 
RUN mkdir /jail/
RUN ln -s /opt/run.sh /bin/run_ftp
CMD run_ftp
EXPOSE 20 21 50000-50010