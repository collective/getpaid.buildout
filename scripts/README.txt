Installation instructions
=========================

Copy the directory/directories within the Products directory to the
Products directory of your zope instance.

Note: if you are using Plone 3.0, you do NOT need the Five and
CMFonFive directories.  If they are in the Products directory of this
download, please ignore them and only copy the PloneGetPaid directory.

In all cases (so both Plone 2.5 and 3.0), copy the directories within
the lib/python directory to the lib/python directory of your zope
instance.  (On Windows: lib\python.)

Also, you will need the following python packages:

- simplejson
- dateutil

Install them with the standard package tools available for your
platform or with easy-install.


For further instructions and more info see the readme.txt file in
the PloneGetPaid dir within Products.
