from zope.component import getUtility, queryAdapter, adapts
from zope.app.component.hooks import getSite
from zope import interface, schema

from z3c.form import form, field, button
from z3c.form.interfaces import IFormLayer, HIDDEN_MODE
from plone.z3cform.layout import FormWrapper, wrap_form
from plone.z3cform import z2
from Products.Five.browser import BrowserView

from getpaid.core.interfaces import IShoppingCartUtility, IOffsitePaymentProcessor

class CheckoutButton(BrowserView):
    """page for NMI button
    """
    
    def ccnumber_view_url(self):
        return getSite().absolute_url() + '/@@getpaid.nmi.ccnumber'
    
class CheckoutCCNumberSchema(interface.Interface):
    ccnumber = schema.TextLine(title=u"Credit Card Number")
    ccexp = schema.TextLine(title=u"Expiration")

class CheckoutProcessorSchema(interface.Interface):
    # hidden fields received from request
    type = schema.TextLine()
    amount = schema.TextLine()
    redirect = schema.TextLine()
    key_id = schema.TextLine()
    time = schema.TextLine()
    orderid = schema.TextLine()

class CheckoutCCNumberForm(form.Form):
    fields = field.Fields(CheckoutCCNumberSchema)
    fields += field.Fields(CheckoutProcessorSchema, mode = HIDDEN_MODE)
    ignoreContext = True # don't use context to get widget data
    label = u"Please enter your credit card information"
    prefix = '' # NMI external processor needs unprefixed fields

    @button.buttonAndHandler(u'Network Merchants Secure Payment')
    def handlePay(self, action):
        pass
    
class CheckoutWidgets(field.FieldWidgets):
    adapts(CheckoutCCNumberForm, IFormLayer, interface.Interface)
    
    prefix = '' # NMI external processor needs unprefixed fields
    
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
        
    def contents(self):
        """This is the method that'll call your form.  You don't
        usually override this.
        """
        # A call to 'switch_on' is required before we can render
        # z3c.forms within Zope 2.
        z2.switch_on(self, request_layer=self.request_layer)
        self.request.getURL = self.processor.server_url
        return self.render_form()

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
