"""
    kaptan
    ~~~~~~

    :copyright: (c) 2013-2016 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from setuptools import find_packages, setup

about = {}
with open("kaptan/__about__.py") as fp:
    exec(fp.read(), about)


setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=find_packages(),
    url=about['__url__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__description__'],
    install_requires=['PyYAML'],
    entry_points=dict(
        console_scripts=[
            'kaptan = kaptan:main',
        ],
    ),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
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

