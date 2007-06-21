from glob import glob
import os
import shutil
import logging

class Cleanup (object):
    def __init__ (self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.logger = logging.getLogger (self.name)
        self.eggs = buildout['buildout']['eggs-directory']

    def install (self):
        glob_expr = os.path.join (self.eggs, 'zope*')
        self.logger.info ("going to remove %r", glob_expr)
        for filename in glob (glob_expr):
            self.logger.debug ("removing %r", filename)
            shutil.rmtree (filename)
        return []
