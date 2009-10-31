# Copyright (c) 2007 ifPeople, Juan Pablo Giménez, and Contributors
#
"""
"""

from getpaid.core.options import PersistentOptions
from getpaid.nmi.interfaces import IOptions

Options = PersistentOptions.wire("NMIOptions",
                                 "getpaid.nmi",
                                 IOptions)

