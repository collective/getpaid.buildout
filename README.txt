GetPaid Development Buildout
============================

This buildout is intended for the developers working on GetPaid.

Basic Use
---------

If you just want to try out GetPaid trunk, run:

$ python bootstrap.py -c 334.cfg
(use Python 2.4 for Plone 3 and Python 2.6 for Plone 4)
$ bin/buildout -c 334.cfg
(to get GetPaid working on Plone 3.3.4)

Re-running buildout will run svn up for all of the checked out packages.

By default, only Products.PloneGetPaid and getpaid.core are checked out from
version control.  The other packages are installed from the released
versions on PyPI.

If you want to check out additional packages, create a local.cfg file that
extends 3.3.4.cfg and lists additional packages to check out. (The branch
locations for these packages are defined in sources.cfg)

[buildout]
extends = 3.3.4.cfg
auto-checkout =
    getpaid.paypal


Buildout Structure
------------------

sources.cfg        Defines package locations in version control
base.cfg           A basic buildout to install Zope and Plone with the getpaid packages.
                   Extends sources.cfg.
334.cfg            Extends base.cfg with Plone 3-specific configuration.
4.0a5.cfg          Experimental buildout for work on Plone 4 compatibility.
