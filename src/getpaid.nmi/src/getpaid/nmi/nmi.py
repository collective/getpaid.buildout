"""
"""
import md5
from datetime import datetime
from cPickle import loads, dumps
from AccessControl import getSecurityManager
from zope import component, interface
from zope.component import getUtility
from zope.app.component.hooks import getSite
from getpaid.core.processors import OffsitePaymentProcessor
from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager, \
                                    ILineContainerTotals
from getpaid.core import payment
from getpaid.core.interfaces import IWorkflowPaymentProcessorIntegration
from getpaid.core.order import Order
from getpaid.nmi.interfaces import IOptions

_host = "https://secure.nmi.com/api/transact.php"
_test_key_id = "449510"
_test_key = "\!b2#I/wu%)4_tUdpAxO|GDWW?20:V.w"

class StandardProcessor(OffsitePaymentProcessor):
    name = 'charge-it'
    title = u'Off-site NMI Checkout'
    options_interface = IOptions

    checkout_button = 'getpaid.nmi.checkout-button'

    type = 'sale'
    
    def server_url(self):
        return _host

    @property
    def key_id(self):
        if getattr(self.options, "server_url", "Test") == "Test":
            key = _test_key_id
        else:
            key = self.options.merchant_id
        return key

    @property
    def key(self):
        if getattr(self.options, "server_url", "Test") == "Test":
            key = _test_key
        else:
            key = self.options.merchant_key
        return key

    def ipn_url(self):
        return getSite().absolute_url() + '/@@getpaid.nmi.ipnreactor'

    def hash(self):
        key = self.key
        time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        orderid = self.orderid()
        m = md5.new()
        m.update("%s|%s|%s|%s" % (orderid,
                                  self.amount(),
                                  time,
                                  key))
        return {'value': m.hexdigest(),
                'time': time,
                'orderid': orderid}

    def amount(self):
        cartutil=getUtility(IShoppingCartUtility)
        cart=cartutil.get(getSite())
        total = ILineContainerTotals(cart).getTotalPrice()
        return '%.2f' % total

    def orderid(self):
        cartutil=getUtility(IShoppingCartUtility)
        cart=cartutil.get(getSite())
        # we'll get the order_manager, create the new order, and store it.
        order_manager = getUtility(IOrderManager)
        new_order_id = order_manager.newOrderId()
        order = Order()
        
        # register the payment processor name to make the workflow handlers happy
        order.processor_id = 'getpaid.nmi.processor'

        # FIXME: registering an empty contact information list for now - need to populate this from user
        # if possible
        order.contact_information = payment.ContactInformation()
        order.billing_address = payment.BillingAddress()
        order.shipping_address = payment.ShippingAddress()

        order.order_id = new_order_id
        
        # make cart safe for persistence by using pickling
        order.shopping_cart = loads(dumps(cart))
        order.user_id = getSecurityManager().getUser().getId()

        order.finance_workflow.fireTransition('create')
#        order.finance_workflow.fireTransition('authorize')
        
        order_manager.store(order)

        return order.order_id
