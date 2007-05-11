========
ploneout
========

by Hanno Schlichting, Martin Aspeli et. al.

'ploneout' is a "buildout" for Zope 2 and Plone. It helps you set up a
Zope 2.9 instance, with Plone 2.5 installed. You can also use it as a starting
point for your own projects, creating your own "buildout" to manage your
particular packages and configuration.

Additional requirements
-----------------------

You need to have an unrestricted internet access for the first time you build
your environment. Otherwise you might get some rather cryptic errors in urllib2,
which suggest that it couldn't download some of the required tarballs.

The only Plone dependency besides Python itself, that is not currently tracked
with ploneout is the Python Imaging Library (PIL). As it requires a lot of
secondary development libraries to be installed on your system in order to be
able to compile the Python C extensions, you better use your OS specific
package management tools to install it.

For a list of available Windows installers, have a look at
    http://effbot.org/downloads/#PIL. If you are on a Mac using MacPorts you can
use "sudo port install py-pil" if you use the MacPorts provided Python as a base
for your ploneout.

How do I use it?
----------------

Run the following command from the getpaid.buildout directory:

 $ python bootstrap.py

This creates a few directories used by buildout. Then run:

 $ bin/buildout -v

The -v isn't necessary, but may make you feel better in the knowledge that
a lot is going on.

This will take a long time and use up to 200Mb of disk space. It will:

 - Create the 'parts' directory
 - Create a directory var where your Data.fs will live.
 - Download a Zope 2 tarball into parts/zope2.
 - Build Zope 2, using 'setup.py build_ext -i'
 - Build a Zope 2 instance in parts/instance
 - Install Plone 2.5's products into the Zope 2 instance

If you've done this once, you can speed up the process by running

 $ bin/buildout -o

This tells buildout that you do not want it to go online and check for updates.

To start Zope 2, you can now do:

 $ bin/instance fg

If you wish to have an interactive python prompt that has all the packages
Zope is aware of, e.g. for testing purposes, you can run:

 $ bin/zopepy

What's going on?
----------------

'ploneout' uses 'zc.buildout'. You can read more about zc.buildout on its
pypi page: http://python.org/pypi/zc.buildout

In brief, buildout depends on two things:

 - Python eggs with entry points that define "recipes"
 - A buildout.cfg file that pieces together these recipes into a script
 
When you run bin/buildout, it parses buildout.cfg. Let's look at that file:

    [buildout]
    ...
    
    parts =
        zope2
        instance
        zopepy

    find-links =
        http://download.zope.org/distribution/
        http://effbot.org/downloads

    eggs =
        elementtree

    [zope2]
    recipe = z2c.recipe.zope2install
    url = http://www.zope.org/Products/Zope/2.9.6/Zope-2.9.6-final.tgz

    [instance]
    recipe = z2c.recipe.zope2instance
    zope2-location = ${zope2:location}
    user = admin:admin
    debug-mode = on
    eggs =
        ${buildout:eggs}
        ...

    products =
        ${buildout:directory}/products

    [zopepy]
    recipe = zc.recipe.egg
    eggs = ${instance:eggs}
    interpreter = zopepy
    extra-paths = ${zope2:location}/lib/python
    scripts = zopepy

The main section is '[buildout]', which defines the 'parts' that will make up
this buildout, in the order that they will be executed. It also specifies a
number of eggs that should be installed within the self-contained python
environment that buildout creates (these will be downloaded from pypi as
necessary) in the 'eggs' parameter. There is also a list of URLs under 
'find-links', which helps buildout download eggs not found in the standard
pypi repository.

The first part is 'zope2', and you will see the corresponding definition in 
the '[zope2]' section. This, like all sections, first defines the 'recipe' 
that should be used. The recipe is the name of an egg, which will be
downloaded from pypi if possible. It could also come from the eggs listed
under 'develop'.

After the recipe definition, each part may have a number of options. Here is
what happens:

 1. The zope2 part uses the z2c.recipe.zope2install recipe. This egg, by
    way of an entry point, will execute some Python code that downloads a
    Zope 2 release tarball on the URL specified in the 'url' parameter, and
    puts it in 'parts/zope2'.

 2. Next the instance part is executed, using z2c.recipe.zope2instance. This
    creates a Zope 2 instance from the Zope 2 download created with the zope2
    part, and patches its etc/zope.conf file a little. There are a number of
    parameters in play:

      zope2-location -- specifies the Zope checkout or extracted tarball which
      should be used to create the instance. You can use the one checked out by
      the z2c.recipe.zope2install or use one already found on your system.

      user -- sets the username and password for the root Zope user

      debug-mode -- Set to 'off' if you don't want to use debug mode
      (recommended for production servers)

      verbose-security -- Set to 'on' to turn on verbose security settings.
      Again, this is not recommended for production servers. This has the side
      effect of setting "security-policy-implementation python"

      eggs -- lists a number of eggs that will be available at runtime when
      Zope is started up.

      products -- specifies the directories which will house the products for
      the instance. zope.conf is patched so that Zope does not only look for
      products under $INSTANCE_HOME/products, but also in these directories.
      One additional directory is found at the root of the buildout. This is
      done so that the instance can be re-created from scratch more easily.

 3. Finally, the zopepy part sets up a custom python interpreter (or rather,
    a script which launches Python with the correct paths set) which will have
    available the various packages that buildout prepares for Zope. This is 
    useful for testing.

How do I use this for my own projects?
--------------------------------------

It is not terribly difficult to write new recipes (especially if you can learn
by example), and it's easier still to write your own buildout.cfg files. To
simple use 'ploneout' for your own projects, though, all you should need
to do is:

 - copy the whole of ploneout to a new directory, probably with a different 
   name

 - create your own eggs in 'src/'. You may want to use PasteScript and 
   ZopeSkel for this. See http://plone.org/documentation/how-to/use-paster

 - edit buildout.cfg to list your eggs and set any project-specific options

Then you simply run bootstrap.py and bin/buildout as above. You can re-run
bin/buildout when your configuration changes to re-configure your buildout.

The advantage of this, of course, is that you can then replicate your own
buildout across different machines (e.g. to a server or between developers).
