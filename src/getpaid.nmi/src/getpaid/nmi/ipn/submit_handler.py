import logging
import md5

from zope.app.component.hooks import getSite
from Products.Five.browser import BrowserView
from zope.component import getUtility, queryAdapter

from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager, \
                                    IOffsitePaymentProcessor

logger = logging.getLogger("getpaid.nmi")

class Listener(BrowserView):
    """Listener for NMI IPN notifications - registered as a page view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal = getSite()
    
    def process(self):
        cartutil=getUtility(IShoppingCartUtility)
        cart=cartutil.get(self.portal, create=True)
        processor = queryAdapter(cart, IOffsitePaymentProcessor, 'getpaid.nmi.processor')
        processor.options = processor.options_interface(self.portal)
        
        is_valid_IPN = self.verify(processor.key)
        if not is_valid_IPN:
            logger.debug('received bogus IPN')
            return
        form = self.request.form
        orderid = form['orderid']
        response = form['response']
        order_manager = getUtility(IOrderManager)
        if orderid in order_manager:
            order = order_manager.get(orderid)
            if response == '1': # Approved
                order.finance_workflow.fireTransition('charge-charging')
                cartutil.destroy(self.context)
                logger.debug('received successful IPN payment notification for order %s' % orderid)
                return self.request.response.redirect('%s/@@getpaid.nmi.thank-you?orderid=%s' %
                                                      (self.portal.absolute_url(), orderid))
            elif response == '2': # Declined
                order.finance_workflow.fireTransition('decline-charging')
                logger.debug('received unsuccessful IPN payment notification for order %s' % orderid)
                return
            else: # Error
                logger.debug('Error in transaction')
                return
        # invoice not in cart
        logger.debug('received IPN that does not apply to any order number - order "%s"' % orderid)
        return 
        
    def compare_cart(self, notification, order):
        for ref in order.shopping_cart.keys():
            cart_item = order.shopping_cart[ref]
            if notification.shopping_cart.has_key(cart_item.product_code):
                notification_item = notification.shopping_cart[cart_item.product_code]
                if int(cart_item.quantity) != int(notification_item.quantity):
                    return False
            else:
                # item not in returned cart - invalid IPN response
                return False
        # everything checks out
        return True
            


    def verify(self, key):
        form = self.request.form
        m = md5.new()
        m.update("%s|%s|%s|%s|%s|%s|%s|%s" % (form['orderid'], form['amount'],
                                              form['response'], form['transactionid'],
                                              form['avsresponse'], form['cvvresponse'],
                                              form['time'], key))        
        if form['hash'] == m.hexdigest():
            return True
        else:
            return False
