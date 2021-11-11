# -*- coding: utf-8 -*-

# Copyright 2020-2021 Kungliga Tekniska högskolan

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function, unicode_literals

__all__ = ["MailReceiver"]

import logging
import time

from systemd import journal

MAIL_MESSAGE_ID = '6418d3c9-92e9-4952-abf6-60bbdb20314f'

class MailReceiver():
    def __init__(self, filterconf):
        self.filterconf = filterconf
        self.logger = logging.getLogger("sms")
        self.errors = 0

    def process(self, queue_id, peer, envelope_sender, envelope_recipient, msg):
        if msg.is_multipart():
            raise Exception(f"Multipart messages not supported yet.")

        def journal_header(s):
            return "MAIL_HEADER_" + s.upper().replace("-","_")
        headers = { journal_header(k):v for k,v in msg.items() }
        text = str(msg.get_body(preferencelist=('plain',)))

        journal.send(text, MESSAGE_ID=MAIL_MESSAGE_ID, MAIL_QUEUE_ID=queue_id, **headers)

        return "Message logged in Journal."

