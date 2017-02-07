# Copyright (c) 2016 WebDevEngines LLC.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import unicode_literals

import os
import requests
import sys
import logging

from pyftpdlib.authorizers import (
    DummyAuthorizer,
    AuthenticationFailed
)
from pyftpdlib.handlers import (
    FTPHandler,
    TLS_FTPHandler
)
from pyftpdlib.servers import FTPServer


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

USERS = {}
WEBHOOKS = {}

BANNER = os.environ.get("BANNER", "FTP Hook")
MAX_CONNS = os.environ.get("MAX_CONNS", 100)
MAX_CONNS_PER_IP = os.environ.get("MAX_CONNS_PER_IP", 5)
PASV_PORT_START = os.environ.get("PASV_PORT_START", 5000)
PASV_PORT_END = os.environ.get("PASV_PORT_END", 5100)
AUTHENTICATION_URL = os.environ.get("AUTHENTICATION_URL", None)
CERT_FILE_PATH = os.environ.get("CERT_FILE_PATH", "ftps.pem")
ENABLE_FTPS = os.environ.get("ENABLE_FTPS", None) == "True"


def on_login(obj, username):
    log.info("Logged In")
    if username not in WEBHOOKS:
        raise Exception("Username not found in WebHook map")
    raw_wh = WEBHOOKS[username]
    if "form_parameter" in raw_wh:
        obj.webhook_form_parameter = raw_wh["form_parameter"]
    else:
        obj.webhook_form_parameter = "file"
    if "url" in raw_wh:
        obj.webhook = raw_wh["url"]
    else:
        raise Exception("WebHook URL is missing")


def on_file_received(obj, _file):
    log.info("File Received")
    f = open(_file)
    log.info("File Opened")
    try:
        log.info("WebHook Request Started")
        r = requests.post(obj.webhook, files={obj.webhook_form_parameter: f})
        log.info("WebHook Status Code: %s" % unicode(r.status_code))
        log.info("WebHook Response: %s" % unicode(r.content))
    except Exception, e:
        log.info("Error: %s" % unicode(e))
    finally:
        f.close()


class WebHookAuthorizer(DummyAuthorizer):
    def validate_authentication(self, username, password, handler):
        r = requests.post(AUTHENTICATION_URL, data={
            "username": username,
            "password": password
        })

        if r.status_code != 200:
            raise AuthenticationFailed
        
        WEBHOOKS[username] = r.json()

    def has_user(self, username):
        return username in USERS.keys()

    def has_perm(self, username, perm, path=None):
        return perm == "w"

    def get_msg_login(self, username):
        return "Welcome"

    def get_msg_quit(self, username):
        return "Bye"

    def get_perms(self, username):
        return "w"

    def get_home_dir(self, username):
        return "/jail/"


def main(port):
    authorizer = WebHookAuthorizer()
    
    if ENABLE_FTPS:
        handler = TLS_FTPHandler
        handler.certfile = CERT_FILE_PATH
        handler.tls_control_required = True
        handler.tls_data_required = True 
    else:
        handler = FTPHandler
    
    handler.on_login = on_login
    handler.on_file_received = on_file_received
    handler.permit_foreign_addresses = True   
    handler.authorizer = authorizer
    handler.banner = BANNER
    handler.passive_ports = range(int(PASV_PORT_START), int(PASV_PORT_END))
    server = FTPServer(("", port), handler)
    server.max_cons = int(MAX_CONNS)
    server.max_cons_per_ip = int(MAX_CONNS_PER_IP)
    server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please pass the desired port"
        exit(-1)
    main(sys.argv[1])
