# Copyright (c) 2007 ifPeople, Juan Pablo Giménez, and Contributors

from Products.Five.browser import BrowserView
from getpaid.core.interfaces import IPaymentProcessor
from zope.component import getAdapter
from zExceptions import Unauthorized
from getpaid.nmi.interfaces import INMIOptions


class Notification(BrowserView):

    def validate_authorization(self):
        auth = self.request._authUserPW()
        if auth is None:
            raise Unauthorized
        else:
            name, password = auth
            options = INMIOptions(self.context)
            if name != options.merchant_id or password != options.merchant_key:
                raise Unauthorized

    def __call__(self):
        self.validate_authorization()
        self.request.stdin.seek(0)
        xml = self.request.stdin.read()
        processor = getAdapter(self.context, IPaymentProcessor,
                               'Google Checkout')
        return processor.notify(xml).toxml(pretty=True)

