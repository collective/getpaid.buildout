Introduction
============

`Google Checkout`_ integration with GetPaid.


Status
======

Working integration with Google Checkout using both the Checkout API
and the Notification API:

- The GetPaid checkout wizard is completely replaced with Google
  Checkout.

- Includes integration with the Google Checkout Notification API. So
  far this is just used to improve the user experience during the
  checkout process. A shopper can still edit the cart after commencing
  the google checkout process - an "edit cart" link is available from
  the checkout. And the cart is cleared after completing the checkout.

- The GetPaid order manager is not integrated with Google Checkout.
  Google Checkout includes its own order management functionality.
  Although Google Checkout does have a rich enough API that these two
  could be integrated with each other. And there is already working
  integration with the Google Checkout Notification API.

- Makes use of zcml overrides to integrate with GetPaid. This is a
  sign that GetPaid is not yet sufficiently plugable to support this
  kind of processor.

- Includes integration with Google Analytics.

- Works with gchecky 0.2.1.


Todo
====

- Update locales.


Demo
====

Google provides a sandbox service that can be used to create a working
demonstration.

Buildout
--------

Use getpaid.buildout to create your own demo of this integration.
Uncomment the various googlecheckout variable substitutions throughout
buildout.cfg::

    ${googlecheckout:develop}
    ${googlecheckout:eggs}

Note - during development, if you're developing locally, make sure to
access your site via 127.0.0.1:8080/my-plone-instance instead of
localhost:8080/my-plone-instance as the latter is considered an
invalid URL by gchecky.


Google Merchant Account
-----------------------

Create a merchant account in the Google Checkout Sandbox service. See
step 1 of `Getting Started with Google Checkout`.

Configure the notification handshake for this merchant account. Set
the API callback URL and enable checking serial numbers for
notification acknowledgments:

1. Log in to your merchant account.

2. Click on the *Settings* tab.

3. Click the *Integration* link on the left side of the page.

4. Make sure "My company will only post digitally signed carts." is
   checked.

5. Enter a URL for the notification callback for your site into *API
   callback URL*. This will look something like::

     http://demo.my.site/google-checkout-notification

   And select "XML" for the "Callback method".

   (This URL can be HTTP for merchant accounts created in the sandbox
   service. However needs to be HTTPS with suitable certificate for
   production.)

6. Expand the list of advanced settings and check the box next to the
   setting that says, "Require notification acknowledgments to specify
   the serial number of the notification."

7. Click the *Save* button to update your settings.


GetPaid Configuration
---------------------

Configure the Google Checkout processor in GetPaid with the Merchant
ID and Merchant Key for the sandbox. You'll find these in "Settings"
-> "Integration" of the `Google Checkout Manager`_.


Google Buyer Account
--------------------

To put through some test purchases you will need a sandbox buyer
account. Google Checkout will not permit you to complete a purchase
from your Google Checkout merchant account while logged in with the
email address associated with your merchant account. In other words,
you cannot buy from yourself, even in sandbox.

To create a new sandbox buyer account,
visit http://sandbox.google.com/checkout


Google Analytics
----------------

If you want to use this with along with Google Analytics then copy the
following snippet to your Plone site by editing "Site Setup" -> "Site
Settings" -> "JavaScript for web statistics support"::

    <script src="http://www.google-analytics.com/ga.js" type="text/javascript"></script>
    <script src="http://checkout.google.com/files/digital/ga_post.js" type="text/javascript"></script>
    <script type="text/javascript">
    <!--
      var pageTracker = _gat._getTracker("UA-XXXXXXX-X");
      pageTracker._initData();
      pageTracker._trackPageview();
      var checkout_forms = cssQuery('form.googlecheckout');
      for (var i=0; i < checkout_forms.length; i++) {
        checkout_forms[i].onsubmit = function(e) {
          setUrchinInputCode(pageTracker);
        };
      };
    //-->
    </script>

You will need to replace ``UA-XXXXXXX-X`` with your own Google
Analytics account number.


.. _Google Checkout:
   http://code.google.com/apis/checkout/developer/index.html

.. _Getting Started with Google Checkout:
   http://code.google.com/apis/checkout/developer/index.html#integration_overview

.. _Google Checkout Manager:
   http://sandbox.google.com/checkout/sell
