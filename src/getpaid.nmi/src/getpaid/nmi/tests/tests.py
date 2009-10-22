import unittest
from Testing import ZopeTestCase
from zope.testing import doctest
from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
import Products.PloneGetPaid
import getpaid.nmi
from Products.Five import zcml
from xml.dom.minidom import parseString


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_UDIFF)


class NMIFuncationalTestCase(PloneGetPaidFunctionalTestCase):

    def afterSetUp(self):
        super(NMIFuncationalTestCase, self).afterSetUp()
        zcml.load_config('configure.zcml', package=getpaid.nmi)
        zcml.load_config('testing.zcml', package=getpaid.nmi.tests)
        zcml.load_config('configure.zcml', package=Products.PloneGetPaid)
        self.portal.portal_quickinstaller.installProduct('PloneGetPaid')

    def extract_data(self, xml_blob, name):
        xml = parseString(xml_blob)
        return str(xml.getElementsByTagName(name)[0].firstChild.data).strip()


def test_suite():
    return unittest.TestSuite([
        ZopeTestCase.ZopeDocFileSuite(
            'nmi.txt',
            package='getpaid.nmi',
            test_class=NMIFuncationalTestCase,
            optionflags=OPTIONFLAGS,
            ),
        ZopeTestCase.ZopeDocFileSuite(
            'nmi-browser.txt',
            package='getpaid.nmi',
            test_class=NMIFuncationalTestCase,
            optionflags=OPTIONFLAGS,
            ),
        ])
