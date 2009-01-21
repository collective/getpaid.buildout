"""
"""

from getpaid.core.options import PersistentOptions
import interfaces

PaypalPayFlowProOptions = PersistentOptions.wire("PaypalPayFlowProOptions",
                                                 "getpaid.payflowpro",
                                                 interfaces.IPaypalPayFlowProOptions )

