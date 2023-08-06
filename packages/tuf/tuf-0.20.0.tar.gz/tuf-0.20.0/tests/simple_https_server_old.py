#!/usr/bin/env python

# Copyright 2014 - 2017, New York University and the TUF contributors
# SPDX-License-Identifier: MIT OR Apache-2.0

"""
<Program>
  simple_https_server_old.py

<Author>
  Vladimir Diaz.

<Started>
  June 17, 2014

<Copyright>
  See LICENSE-MIT OR LICENSE for licensing information.

<Purpose>
  Provide a simple https server that can be used by the unit tests.  For
  example, 'download.py' can connect to the https server started by this module
  to verify that https downloads are permitted.

<Reference>
  ssl.SSLContext.wrap_socket:
    https://docs.python.org/3/library/ssl.html#ssl.SSLContext.wrap_socket

  SimpleHTTPServer:
    http://docs.python.org/library/simplehttpserver.html#module-SimpleHTTPServer
"""

import sys
import ssl
import os
import http.server

keyfile = os.path.join('ssl_certs', 'ssl_cert.key')
certfile = os.path.join('ssl_certs', 'ssl_cert.crt')


if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    certfile = sys.argv[1]

httpd = http.server.HTTPServer(('localhost', 0),
   http.server.SimpleHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile, keyfile)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

port_message = 'bind succeeded, server port is: ' \
    + str(httpd.server_address[1])
print(port_message)

if len(sys.argv) > 1 and certfile != sys.argv[1]:
  print('simple_https_server_old: cert file was not found: ' + sys.argv[1] +
      '; using default: ' + certfile + " certfile")

httpd.serve_forever()
