import md5
from datetime import datetime
from cPickle import loads, dumps

from AccessControl import getSecurityManager
from zope.component import getUtility, queryAdapter
from zope.app.component.hooks import getSite
from zope import interface, schema

from z3c.form import form, field, button
from plone.z3cform.layout import FormWrapper, wrap_form
from Products.Five.browser import BrowserView

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager, \
                                    ILineContainerTotals, IOffsitePaymentProcessor
from getpaid.core.order import Order
from getpaid.core import payment

class CheckoutButton(BrowserView):
    """page for NMI button
    """
    
    def ccnumber_view_url(self):
        return getSite().absolute_url() + '/@@getpaid.nmi.ccnumber'
    
class CheckoutCCNumberSchema(interface.Interface):
    ccnumber = schema.TextLine(title=u"Credit Card Number")
    ccexp = schema.TextLine(title=u"Expiration")

class CheckoutCCNumberForm(form.Form):
    fields = field.Fields(CheckoutCCNumberSchema)
    ignoreContext = True # don't use context to get widget data
    label = u"Please enter your credit card information"

class CheckoutCCNumberWrapper(FormWrapper):
    """page for NMI button
    """

    def __init__(self, context, request):
        super(CheckoutCCNumberWrapper, self).__init__(context, request)
        self.portal = context
        self.portal_url = self.portal.absolute_url()
        cartutil=getUtility(IShoppingCartUtility)
        cart=cartutil.get(self.portal, create=True)
        self.processor = queryAdapter(cart, IOffsitePaymentProcessor, 'getpaid.nmi.processor')
        self.processor.options = self.processor.options_interface(self.portal)
        
    def action_url(self):
        return self.processor.server_url
        
    def key_id(self):
        return self.processor.key_id

    def amount(self):
        cartutil=getUtility(IShoppingCartUtility)
        cart=cartutil.get(self.portal)
        total = ILineContainerTotals(cart).getTotalPrice()
        return '%.2f' % total

    def hash(self):
        key = self.processor.key
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

    def return_url(self):
        return self.portal_url + '/@@getpaid.nmi.thank-you'

    def ipn_url(self):
        return self.portal_url + '/@@getpaid.nmi.ipnreactor'

    def orderid(self):
        cartutil=getUtility(IShoppingCartUtility)
        cart=cartutil.get(self.portal)
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
        order.finance_workflow.fireTransition('authorize')
        
        order_manager.store(order)

        return order.order_id

CheckoutCCNumber = wrap_form(CheckoutCCNumberForm, CheckoutCCNumberWrapper)

class Thankyou(BrowserView):
    """Class for overriding getpaid-thank-you view
    """
    
    def getInvoice(self):
        if self.request.has_key('orderid'):
            return self.request['orderid']
        else:
            return None

    def getURL(self):
        portal_url = getSite().absolute_url()
        if self.getInvoice() is not None:
            return "%s/@@getpaid-order/%s" % ( portal_url, self.getInvoice())
        else:
            return ''
