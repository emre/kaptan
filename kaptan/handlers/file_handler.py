# -*- coding: utf8 -*-
"""
    kaptan.handlers.file_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

import os
import sys
import os.path as op

from . import BaseHandler


def import_pyfile(pathname, mod_name=''):
    """Import the contents of filepath as a Python module.

    Parameters
    ----------
    pathname: str
        Path to the .py file to be imported as a module

    mod_name: str
        Name of the module when imported

    Returns
    -------
    mod
        The imported module

    Raises
    ------
    IOError
        If file is not found
    """
    if not op.isfile(pathname):
        raise IOError('File {0} not found.'.format(pathname))

    if sys.version_info[0] == 3:
        import importlib.machinery
        if sys.version_info[1] <= 2:
            load_func = importlib.abc.SourceLoader
        else:
            load_func = importlib.machinery.SourceFileLoader
        loader = load_func('', pathname)
        mod = loader.load_module(mod_name)
    else:
        import imp
        mod = imp.load_source(mod_name, pathname)
    return mod


class FileHandler(BaseHandler):

    def load(self, file_):
        module = import_pyfile(file_)
        data = dict()
        for key in dir(module):
            value = getattr(module, key)
            if not key.startswith("__"):
                data.update({key: value})
        return data

    def dump(self, file_):
        raise NotImplementedError("Exporting python files is not supported.")
