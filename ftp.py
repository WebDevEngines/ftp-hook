# Copyright (c) 2016 WebDevEngines LLC.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import os
import requests
import sys
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


WEB_HOOK = os.environ.get("WEB_HOOK", None)
FTP_USERNAME = os.environ.get("FTP_USERNAME", None)
FTP_PASSWORD = os.environ.get("FTP_PASSWORD", None)
WEB_HOOK_FORM_PARAMETER = os.environ.get("WEB_HOOK_FORM_PARAMETER", None)


class WebHookHandler(FTPHandler):
    def on_file_received(self, _file):
        log.info("File Received")
        f = open(_file)
        log.info("File Opened")
        try:
            log.info("WebHook Request Started")
            r = requests.post(WEB_HOOK, files={WEB_HOOK_FORM_PARAMETER: f})
            log.info("WebHook Status Code: %s" % str(r.status_code))
            log.info("WebHook Response: %s" % str(r.content))
        except Exception, e:
            log.info("Error: %s" % str(e))
        finally:
            f.close()


def main(port):
    log.info("WebHook: '%s'" % WEB_HOOK)
    log.info("FormParameter: '%s'" % WEB_HOOK_FORM_PARAMETER)
    handler = WebHookHandler
    handler.authorizer = DummyAuthorizer()
    handler.authorizer.add_user(FTP_USERNAME, FTP_PASSWORD, '/jail/', perm='w')
    handler.banner = "FTP Hook"
    server = FTPServer(("", port), handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please pass the desired port"
        exit(-1)
    main(sys.argv[1])
