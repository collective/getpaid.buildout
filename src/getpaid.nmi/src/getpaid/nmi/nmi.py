"""
"""
import md5
from DateTime import DateTime
from getpaid.core.processors import OffsitePaymentProcessor
from getpaid.nmi.interfaces import IOptions

_host = "https://secure.nmi.com/api/transact.php"
_test_key_id = "449510"
_test_key = "\!b2#I/wu%)4_tUdpAxO|GDWW?20:V.w"

class StandardProcessor(OffsitePaymentProcessor):
    name = 'charge-it'
    title = u'Off-site NMI Checkout'
    options_interface = IOptions

    checkout_button = 'getpaid.nmi.checkout-button'

    @property
    def server_url(self):
        return _host

    @property
    def key_id(self):
        if self.options.server_url == "Test":
            key = _test_key_id
        else:
            key = self.options.merchant_id
        return key

    @property
    def key(self):
        if self.options.server_url == "Test":
            key = _test_key
        else:
            key = self.options.merchant_key
        return key
#
#from zope.interface import implements
#from zope.component import getUtility
#
#from getpaid.core.interfaces  import IShoppingCartUtility
#from getpaid.nmi.interfaces import INMIOptions
#from getpaid.nmi.interfaces import INMIWizard
#from getpaid.nmi.interfaces import INMIController
#from getpaid.nmi.interfaces import INMIShipping
#
#from cgi import escape
#
#
#def gcart_item(entry, options):
#    return gmodel.item_t(
#        name = entry.name,
#        description = entry.description,
#        unit_price = gmodel.price_t(
#            value = entry.cost,
#            currency = options.currency,
#            ),
#        quantity = entry.quantity,
#        merchant_item_id = entry.product_code,
#        )
#
#
#class NMIWizard(object):
#
#    implements(INMIWizard)
#
#    options_interface = INMIOptions
#    checkout_button_view_name = 'getpaid-nmi-checkout-button'
#
#    def __init__( self, context ):
#        self.context = context
#        self._controller = None
#
#    def getController( self ):
#        if self._controller is None:
#            self._controller = INMIController(self.context)
#        return self._controller
#
#    controller = property(getController)
#
#    def checkout_shopping_cart(self, cart, analytics_data=None):
#        options = INMIOptions(self.context)
#        cart_key = getUtility(IShoppingCartUtility).getKey(self.context)
#        edit_cart_url = '%s/getpaid-cart' % self.context.absolute_url()
#        continue_shopping_url = self.context.absolute_url()
#        return gmodel.checkout_shopping_cart_t(
#            shopping_cart = gmodel.shopping_cart_t(
#                items = [gcart_item(entry, options) for entry in cart.values()],
#                merchant_private_data={'cart-key': cart_key},
#                ),
#            checkout_flow_support = gmodel.checkout_flow_support_t(
#                shipping_methods = INMIShipping(self.context)(cart),
#                analytics_data = analytics_data,
#                edit_cart_url = edit_cart_url,
#                continue_shopping_url = continue_shopping_url,
#                ),
#            )
#
#    def checkout(self, cart, analytics_data=None):
#        checkout_shopping_cart = self.checkout_shopping_cart(cart,
#                                                             analytics_data)
#        request = checkout_shopping_cart.toxml()
#        response = self.controller.send_xml(request)
#        __traceback_supplement__ = (TracebackSupplement, request, response)
#        return gxml.Document.fromxml(response).redirect_url
#
#    def notify(self, xml):
#        __traceback_supplement__ = (NotifyTracebackSupplement, xml)
#        return self.controller.receive_xml(xml)
#
#
#
#
#class TracebackSupplement:
#
#    def __init__(self, request, response):
#        self.request = request
#        self.response = response
#
#    def format_text(self, name):
#        value = getattr(self, name)
#        return '   - %s:\n      %s' % (name, value.replace('\n', '\n      '))
#
#    def format_html(self, name):
#        value = getattr(self, name)
#        return '<dt>%s:</dt><dd><pre>%s</pre></dd>' % (name, escape(value))
#
#    def getInfo(self, as_html=0):
#        if not as_html:
#            return '%s\n%s' % (self.format_text('request'),
#                               self.format_text('response'))
#        else:
#            return '<dl>%s%s</dl>' % (self.format_html('request'),
#                                      self.format_html('response'))
#
#
#class NotifyTracebackSupplement(TracebackSupplement):
#
#    def __init__(self, xml):
#        self.xml = xml
#
#    def getInfo(self, as_html=0):
#        if not as_html:
#            return '%s' % self.format_text('xml')
#        else:
#            return '<dl>%s</dl>' % self.format_html('xml')
