# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from getpaid.nmi.controller import NMIController
import xml.dom.minidom

_requests = []

class TestingController(NMIController):

    def send_xml(self, msg):
        if 'checkout-shopping-cart' in msg:
            self.store_request(msg)
            return """<?xml version="1.0" encoding="UTF-8"?>
            <checkout-redirect
                xmlns="http://checkout.google.com/schema/2"
                serial-number="1234">
              <redirect-url>http://sandbox.google.com/checkout</redirect-url>
            </checkout-redirect>"""

    def store_request(self, msg):
        msg = xml.dom.minidom.parseString(msg).toprettyxml('  ')
        _requests.append(msg)

    def get_last_request(self):
        return _requests[-1]
