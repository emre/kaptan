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


def import_pyfile(filepath, mod_name=None):
    """Import the contents of filepath as a Python module.

    Parameters
    ----------
    filepath: str
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
    if not op.exists(filepath):
        raise IOError('File {} not found.'.format(filepath))

    if sys.version_info.major == 3:
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader('', filepath)
        mod = loader.load_module(mod_name)
    else:
        import imp
        mod = imp.load_source(mod_name, filepath)

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
