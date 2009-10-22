# Copyright (c) 2007 ifPeople, Juan Pablo Giménez, and Contributors
"""
"""

from getpaid.core import interfaces
from zope import schema

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.nmi')

class IStandardProcessor( interfaces.IPaymentProcessor ):
    """
    NMI Standard Processor
    """

class IOptions( interfaces.IPaymentProcessorOptions ):
    """
    NMI Checkout Options
    """
    server_url = schema.Choice(
        title = _(u"Server URL"),
        values = ( "Test", "Production" ),
        )

    merchant_id = schema.ASCIILine( title = _(u"Merchant Id"))
    merchant_key = schema.ASCIILine( title = _(u"Merchant Key"))
