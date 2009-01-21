This package provides paypal payflowpro payment processor functionality for the getpaid
framework.

It uses python-payflowpro for the underlying access to paypal (http://code.google.com/p/python-payflowpro/ & http://pypi.python.org/pypi/python-payflowpro/)

To create a test paypal payproflow account all you need to do is go to https://www.paypal.com/cgi-bin/webscr?cmd=_payflow-gateway-overview-outside and go through the registration flow.  When it asks you for your credit card information, just drop out (close browser) and a test account will be created.

This is only for US accounts.
 
FYI, you can use the same account for both testing and live transactions at the same time, so if you are going to activate the account, create the login id accordingly.

After completing that step you will receive an email with login instructions.

After logging in you should create a seperate user account for getpaid.payflowpro to use.  You must then configure that account information in getpaid's site setup.

TODO
====
- The login information should be encrypted (or minimally obfuscated) and not redisplayed to the user after it is entered.
