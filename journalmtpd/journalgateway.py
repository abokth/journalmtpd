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

__all__ = ["SMSGateway"]

import sys
import logging
import email
import email.policy
import uuid

from ._private.socketlmtpd import LMTPSocketServer

class JournalGateway(LMTPSocketServer):
    """LMTP socket server with Journal delivery"""
    def __init__(self, mailreceiver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mailreceiver = mailreceiver
        self.logger = logging.getLogger("journalmtpd")

    def process_message(self, peer, mailfrom, rcptto, data):
        qid = str(uuid.uuid4())
        try:
            msg = email.message_from_bytes(data, policy=email.policy.default)

            msgid = "unidentified message"
            try:
                message_id = msg.get('Message-ID')
                if message_id is not None:
                    msgid = f"message {message_id}"
            except Exception as e2:
                pass

            try:
                envelope_sender = mailfrom.decode("ascii")
            except Exception as e2:
                self.logger.warning(f"{qid}: {msgid}: Envelope sender was not ASCII: {e2}")
                envelope_sender = mailfrom.decode("ascii", errors='ignore')

            try:
                envelope_recipient = rcptto.decode("ascii")
            except Exception as e2:
                self.logger.warning(f"{qid}: {msgid}: Envelope recipient was not ASCII: {e2}")
                envelope_recipient = rcptto.decode("ascii", errors='ignore')

            try:
                subject = str(msg.get('Subject'))
            except Exception as e2:
                subject = "No subject"

            self.logger.info(f"{qid}: Processing {msgid} from {envelope_sender} to {envelope_recipient}: {subject}")

            res = self.mailreceiver.process(qid, peer, envelope_sender, envelope_recipient, msg)
            return f"250 2.0.0 {qid}: {res}"
        except Exception as e:
            self.logger.error(f"{qid}: {e}")
            return f"451 {qid}: {e}".encode("UTF-8", errors='ignore')

