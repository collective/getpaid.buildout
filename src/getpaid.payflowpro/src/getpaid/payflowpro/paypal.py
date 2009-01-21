"""
"""
import urllib
import logging

from Products.CMFCore.utils import getToolByName
from zope import component
from zope import interface
from zope.app.annotation.interfaces import IAnnotations

from interfaces import IPaypalPayFlowProOptions, IPaypalPayFlowProProcessor

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core import interfaces as GetPaidInterfaces

from payflowpro.classes import CreditCard, Amount, Profile, Address, Tracking, Response, CustomerInfo
from payflowpro.client import PayflowProClient

RESULT = "getpaid.payflowpro.result"
RESPMSG = "getpaid.payflowpro.respmsg"
CVV2_MATCH = "getpaid.payflowpro.cvv2match"
AUTH_CODE = "getpaid.payflowpro.authcode"
LAST_FOUR = "getpaid.payflowpro.cc_last_four"

logger = logging.getLogger('GetPaid.PayFlowPro')

class PayFlowPro( object ):
    interface.implements( IPaypalPayFlowProProcessor )

    options_interface = IPaypalPayFlowProOptions

    _sites = {
        "Sandbox": "https://pilot-payflowpro.paypal.com",
        "Production": "https://payflowpro.paypal.com",
        }

    def __init__( self, context ):
        self.context = context
        self.options = IPaypalPayFlowProOptions( self.context )

    def authorize( self, order, payment ):
        logger.info('Authorize...')
        
        client = PayflowProClient(partner=self.options.partner,
                                  vendor=self.options.vendor,
                                  username=self.options.username,
                                  password=self.options.password,
                                  url_base=self._sites.get(self.options.server_url))

        card_exp_date = payment.cc_expiration.strftime('%m%y') # MMYY
        credit_card = CreditCard(acct=payment.credit_card,
                                 expdate=card_exp_date,
                                 cvv2=payment.cc_cvc)

        ba = order.billing_address
        responses, unconsumed_data = client.authorization(credit_card,
                                                          Amount(amt=order.getTotalPrice(),
                                                                 currency=self.options.currency),
                                                          extras=[Address(street=ba.bill_first_line,
                                                                          city=ba.bill_city,
                                                                          state=ba.bill_state,
                                                                          zip=ba.bill_postal_code)])
        order.processor_order_id = responses[0].pnref

        annotation = IAnnotations(order)
        annotation[GetPaidInterfaces.keys.processor_txn_id] = responses[0].pnref
        annotation[RESULT] = responses[0].result
        annotation[RESPMSG] = responses[0].respmsg
        annotation[CVV2_MATCH] = responses[0].cvv2match
        annotation[AUTH_CODE] = responses[0].authcode
        annotation[LAST_FOUR] = payment.credit_card[-4:]

        if responses[0].result == '0':
            ret = GetPaidInterfaces.keys.results_success
        else:
            ret = responses[0].respmsg

        logger.info("PNREF: %s" % annotation[GetPaidInterfaces.keys.processor_txn_id])
        logger.info("RESULT: %s" % annotation[RESULT])
        logger.info("RESPMSG: %s" % annotation[RESPMSG])
        logger.info("CVV2_MATCH: %s" % annotation[CVV2_MATCH])
        logger.info("AUTH_CODE: %s" % annotation[AUTH_CODE])
        logger.info("LAST_FOUR: %s" % annotation[LAST_FOUR])

        return ret
    
    def capture(self, order, price):
        logger.info('Capture...')

        annotation = IAnnotations(order)
        transaction_id = annotation[GetPaidInterfaces.keys.processor_txn_id]

        client = PayflowProClient(partner=self.options.partner,
                                  vendor=self.options.vendor,
                                  username=self.options.username,
                                  password=self.options.password,
                                  url_base=self._sites.get(self.options.server_url))

        responses, unconsumed_data = client.capture(transaction_id)
        
        annotation[RESULT] = responses[0].result
        annotation[RESPMSG] = responses[0].respmsg

        if responses[0].result == '0':
            ret = GetPaidInterfaces.keys.results_success
        else:
            ret = responses[0].respmsg

        logger.info("PNREF: %s" % annotation[GetPaidInterfaces.keys.processor_txn_id])
        logger.info("RESULT: %s" % annotation[RESULT])
        logger.info("RESPMSG: %s" % annotation[RESPMSG])
        logger.info("LAST_FOUR: %s" % annotation[LAST_FOUR])

        return ret

    def refund(self, order, amount):
        """ XXX Not implemented
        """
        return "Not implemented"
