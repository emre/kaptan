# -*- coding: utf8 -*-
# flake8: NOQA: F40
import sys

PY2 = sys.version_info[0] == 2


if PY2:
    import collections as collections_abc
else:
    import collections.abc as collections_abc
