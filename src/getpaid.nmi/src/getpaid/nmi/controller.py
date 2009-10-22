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

from zope.interface import implements
from gchecky.controller import Controller
from gchecky.controller import ControllerContext
from gchecky import model as gmodel
from gchecky import gxml
from getpaid.nmi.interfaces import INMIOptions
from getpaid.nmi.interfaces import INMIController
from getpaid.core.interfaces import IShoppingCartUtility
from zope.component import getUtility
import logging

logger = logging.getLogger('getpaid.nmi')


class NMIController(Controller):

    implements(INMIController)

    def __init__(self, context):
        self.context = context
        options = INMIOptions(context)
        self.vendor_id = options.merchant_id
        self.merchant_key = options.merchant_key
        self.is_sandbox = options.server_url == 'Sandbox'

    def send_xml(self, message):
        context = ControllerContext(outgoing=True)
        context.message = message
        diagnose = False
        return self._send_xml(message, context, diagnose)

    def new_order(self, notification):
        private_data = notification.shopping_cart.merchant_private_data
        cart_key = private_data['cart-key'].strip()
        cart_utility = getUtility(IShoppingCartUtility)
        cart = cart_utility.get(self.context)
        cart_utility.destroy(self.context, key=cart_key)

    def receive_xml(self, xml):
        notification = gxml.Document.fromxml(xml)
        if notification.__class__ == gmodel.new_order_notification_t:
            self.new_order(notification)
        else:
            logger.debug('Unhandled notification %s\n%s'
                         % (notification.__class__, xml))
        return gmodel.notification_acknowledgment_t(
            serial_number=notification.serial_number)
