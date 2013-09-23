"""
    kaptan
    ~~~~~~

    :copyright: (c) 2011 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from setuptools import setup

setup(
    name='kaptan',
    version='0.5.4',
    packages=['kaptan', 'kaptan.handlers'],
    url='http://github.com/emre/kaptan',
    license='BSD',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Configuration Manager',
    install_requires=['PyYAML', ],
    entry_points=dict(
        console_scripts=[
            'kaptan = kaptan:main',
        ],
    ),
)
