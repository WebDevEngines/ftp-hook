#!/bin/sh

# Copyright (c) 2016 WebDevEngines LLC.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

echo $DOMAIN
cd /opt/
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ftps.key -out ftps.crt -subj "/C=US/ST=CA/L=LG/O=Dis/CN=$DOMAIN" && cat ftps.crt ftps.key > ftps.pem
sudo -E python ftp.py 21