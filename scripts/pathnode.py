""" path.py -

GetPaid Modification of


- A pys60 modification of path.py

because we couldn't find the following online at the time

- Based on Jason Orendorff's path.py version 7 Mar 2004
 See his site at http://www.jorendorff.com/articles/python/path


this is heavily modified from previous, because the previous had a cumbersome api and semantics.

all methods on this are instance methods, we use properties a little more extensively.

new function.. to like relpathto except!!

 we always traverse relative to the path that we are invoked on as opposed to the current working directory.

 
"""

from __future__ import generators

import sys, os, re, shutil , fnmatch, glob, shutil, codecs

__all__ = ['path']

_base = str

class path(_base):
    """ Represents a filesystem path.

    For documentation on individual methods, consult their
    counterparts in os.path.
    """
    
    # --- Special Python methods.
    
    def __repr__(self):
        return 'path(%s)' % _base.__repr__(self)
    
    # Adding a path and a string yields a path.
    def __add__(self, more):
        return path(_base(self) + more)

    def __radd__(self, other):
        return path(other + _base(self))

    # The / operator joins paths.
    def __div__(self, rel):
        return path(os.path.join(self, rel))

    # Make the / operator work even when true division is enabled.
    __truediv__ = __div__

    def getcwd():
        """ Return the current working directory as a path object. """
        return path(os.getcwd())
    getcwd = staticmethod(getcwd)


    # --- Operations on path strings.

    def abspath(self):       return path(os.path.abspath(self))
    def normcase(self):      return path(os.path.normcase(self))
    def normpath(self):      return path(os.path.normpath(self))
    def realpath(self):      return path(os.path.realpath(self))
    def dirname(self):       return path(os.path.dirname(self))

    basename = os.path.basename 

    def _get_namebase(self):
        base, ext = os.path.splitext(self.name)
        return base

    def _get_ext(self):
        f, ext = os.path.splitext(_base(self))
        return ext

    def _get_drive(self):
        drive, r = os.path.splitdrive(self)
        return path(drive)

    parent = property(dirname)
    name = property(basename)
    namebase = property(_get_namebase)  # without .ext
    ext = property(_get_ext)
    drive = property(_get_drive)

    def splitpath(self):
        """ p.splitpath() -> Return (p.parent, p.name). """
        parent, child = os.path.split(self)
        return path(parent), child

    def splitdrive(self):
        """ p.splitdrive() -> Return (p.drive, <the rest of p>)."""
        drive, rel = os.path.splitdrive(self)
        return path(drive), rel

    def splitext(self):
        """ p.splitext() -> Return (p.stripext(), p.ext). """
        filename, ext = os.path.splitext(self)
        return path(filename), ext

    def stripext(self):
        return self.splitext()[0]

    def joinpath(self, *args):
        return path(os.path.join(self, *args))

    def splitall(self):
        parts = []
        loc = self
        while loc != os.curdir and loc != os.pardir:
            prev = loc
            loc, child = prev.splitpath()
            if loc == prev:
                break
            parts.append(child)
        parts.append(loc)
        parts.reverse()
        return parts

    def relpath(self):
        """ Return this path as a relative path,
        based from the current working directory.
        """
        cwd = path(os.getcwd())
        return cwd.relpathto(self)


    def relpathto(self, dest):
        """ Return a relative path from self to dest.

        If there is no relative path from self to dest, for example if
        they reside on different drives in Windows, then this returns
        dest.abspath().
        """
        origin = self.abspath()
        dest = path(dest).abspath()

        orig_list = origin.normcase().splitall()
        # Don't normcase dest!  We want to preserve the case.
        dest_list = dest.splitall()

        if orig_list[0] != os.path.normcase(dest_list[0]):
            # Can't get here from there.
            return dest

        # Find the location where the two paths start to differ.
        i = 0
        for start_seg, dest_seg in zip(orig_list, dest_list):
            if start_seg != os.path.normcase(dest_seg):
                break
            i += 1

        # Now i is the point where the two paths diverge.
        # Need a certain number of "os.pardir"s to work up
        # from the origin to the point of divergence.
        segments = [os.pardir] * (len(orig_list) - i)
        # Need to add the diverging part of dest_list.
        segments += dest_list[i:]
        if len(segments) == 0:
            # If they happen to be identical, use os.curdir.
            return path(os.curdir)
        else:
            return path(os.path.join(*segments))


    # --- Listing, searching, walking, and matching

    def listdir(self, pattern=None):
        """ D.listdir() -> List of items in this directory.

        Use D.files() or D.dirs() instead if you want a listing
        of just files or just subdirectories.

        The elements of the list are path objects.

        With the optional 'pattern' argument, this only lists
        items whose names match the given pattern.
        """
        names = os.listdir(self)
        if pattern is not None:
            names = fnmatch.filter(names, pattern)
        return [self / child for child in names]

    def dirs(self, pattern=None):
        """ D.dirs() -> List of this directory's subdirectories."""
        return [p for p in self.listdir(pattern) if p.isdir()]

    def files(self, pattern=None):
        """ D.files() -> List of the files in this directory."""
        return [p for p in self.listdir(pattern) if p.isfile()]

    def walk(self, pattern=None):
        """ D.walk() -> iterator over files and subdirs, recursively.

        The iterator yields path objects naming each child item of
        this directory and its descendants.  This requires that
        D.isdir().

        This performs a depth-first traversal of the directory tree.
        Each directory is returned just before all its children.
        """
        for child in self.listdir():
            if pattern is None or child.fnmatch(pattern):
                yield child
            if child.isdir():
                for item in child.walk(pattern):
                    yield item

    def walkdirs(self, pattern=None):
        """ D.walkdirs() -> iterator over subdirs, recursively. """
        for child in self.dirs():
            if pattern is None or child.fnmatch(pattern):
                yield child
            for subsubdir in child.walkdirs(pattern):
                yield subsubdir

    def walkfiles(self, pattern=None):
        """ D.walkfiles() -> iterator over files in D, recursively."""
        for child in self.listdir():
            if child.isfile():
                if pattern is None or child.fnmatch(pattern):
                    yield child
            elif child.isdir():
                for f in child.walkfiles(pattern):
                    yield f

    def fnmatch(self, pattern):
        """ Return True if self.name matches the given pattern.

        pattern - A filename pattern with wildcards,
            for example '*.py'.
        """
        return fnmatch.fnmatch(self.name, pattern)

    # --- Reading or writing an entire file at once.
    
    # just open is enough, need no fancy
    def open(self, mode='r'):
        """ Open this file.  Return a file object. """
        return file(self, mode)
    

    # --- Methods for querying the filesystem.

    exists = os.path.exists
    isabs = os.path.isabs
    isdir = os.path.isdir
    isfile = os.path.isfile
    islink = os.path.islink


    getatime = os.path.getatime
    atime = property(getatime)  # last access time

    getmtime = os.path.getmtime
    mtime = property(getmtime)

    getsize = os.path.getsize
    size = property(getsize)

    def stat(self):
        """ Perform a stat() system call on this path. """
        return os.stat(self)

    def lstat(self):
        """ Like path.stat(), but do not follow symbolic links. """
        return os.lstat(self)

    # --- Modifying operations on files and directories

    def utime(self, times):
        """ Set the access and modified times of this file. """
        os.utime(self, times)

    def chmod(self, mode):
        os.chmod(self, mode)

    def rename(self, new):
        os.rename(self, new)

    def renames(self, new):
        os.renames(self, new)


    # --- Create/delete operations on directories

    def mkdir(self, mode=0777):
        os.mkdir(self, mode)

    def makedirs(self, mode=0777):
        os.makedirs(self, mode)

    def rmdir(self):
        os.rmdir(self)

    def removedirs(self):
        os.removedirs(self)


    # --- Modifying operations on files

    def touch(self):
        """ Set the access/modified times of this file to the current time.
        Create the file if it does not exist.
        """
        fd = os.open(self, os.O_WRONLY | os.O_CREAT, 0666)
        os.close(fd)
        os.utime(self, None)

    def remove(self):
        os.remove(self)

    def unlink(self):
        os.unlink(self)


    # --- High-level functions from shutil

    copyfile = shutil.copyfile    # poor, littel shutil in pys60
    copymode = shutil.copymode
    copystat = shutil.copystat
    copy = shutil.copy
    copy2 = shutil.copy2
    copytree = shutil.copytree
    rmtree = shutil.rmtree


    # --- Special stuff from os

    #if hasattr(os, 'startfile'):
    #    def startfile(self):
    #        os.startfile(self)
    
    # Should I add appuifw.Content_handler() and e32.start_exe() ?
