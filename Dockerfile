# Copyright (c) 2016 WebDevEngines LLC.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM ubuntu:14.04
MAINTAINER WebDevEngines LLC <n.crafford@webdevengines.com>
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d
RUN sudo apt-get update && sudo apt-get install -y build-essential python python-pip
RUN sudo pip install pyftpdlib
USER root
RUN chmod 777 /opt/ 
ADD . /opt/
RUN chmod -R 777 /opt/ 
RUN mkdir /jail/
RUN sudo ln -s /opt/run.sh /bin/run_ftp
CMD run_ftp
EXPOSE 20 21 50000-50010