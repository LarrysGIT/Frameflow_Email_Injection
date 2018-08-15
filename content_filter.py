#!/bin/env python

import email
import sys
import smtplib
import re
import codecs
import quopri

file = sys.argv[1]

msg = email.message_from_file(codecs.open(file))

newmail = False
try:
    for payload in msg.get_payload():
        if payload.get_content_type() == "text/html" and re.search("(?i)frameflow@xxx.yyy.zzz", msg.get("From")):
            newmail = True
            payload.set_payload(quopri.encodestring(payload.get_payload()))
            payload.add_header("Content-Transfer-Encoding", "quoted-printable")
            payload.replace_header("Content-Type", "text/html; charset=us-ascii")
except:
    pass

if newmail:
    codecs.open(file, "w").write(str(msg))

exit(0)
