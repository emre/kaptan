"""
    kaptan
    ~~~~~~

    :copyright: (c) 2013-2016 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

import sys

from setuptools import find_packages, setup

about = {}
with open("kaptan/__about__.py") as fp:
    exec(fp.read(), about)

with open('requirements/base.txt') as f:
    install_reqs = [line for line in f.read().split('\n') if line]

with open('requirements/test.txt') as f:
    tests_reqs = [line for line in f.read().split('\n') if line]

if sys.version_info < (2, 7):
    install_reqs += ['argparse']

if sys.version_info[0] > 2:
    readme = open('README.rst', encoding='utf-8').read()
else:
    readme = open('README.rst').read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=find_packages(),
    url=about['__url__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__description__'],
    long_description=readme,
    install_requires=install_reqs,
    tests_require=tests_reqs,
    entry_points=dict(
        console_scripts=[
            'kaptan = kaptan:main',
        ],
    ),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ),
)

