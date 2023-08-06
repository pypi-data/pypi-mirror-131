# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyrepr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'easyrepr',
    'version': '0.4.0',
    'description': 'Python decorator to automatically generate repr strings',
    'long_description': "========\neasyrepr\n========\n\n.. image:: https://badge.fury.io/py/easyrepr.svg\n   :alt: PyPI\n   :target: https://pypi.org/project/easyrepr/\n.. image:: https://circleci.com/gh/chrisbouchard/easyrepr/tree/main.svg?style=shield\n   :alt: CircleCI\n   :target: https://circleci.com/gh/chrisbouchard/easyrepr/tree/main\n.. image:: https://readthedocs.org/projects/easyrepr/badge/\n   :alt: Read the Docs\n   :target: https://easyrepr.readthedocs.io/en/latest/\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\nPython decorator to automatically generate repr strings\n\n\nExample\n=======\n\n.. code-block:: pycon\n\n   >>> from easyrepr import easyrepr\n   ...\n   >>> class UseEasyRepr:\n   ...     def __init__(self, foo, bar):\n   ...         self.foo = foo\n   ...         self.bar = bar\n   ...\n   ...     @easyrepr\n   ...     def __repr__(self):\n   ...         ...\n   ...\n   >>> x = UseEasyRepr(1, 2)\n   >>> repr(x)\n   'UseEasyRepr(foo=1, bar=2)'\n\n\nInstallation\n============\n\nEasyrepr is `available on PyPI`_, so the easiest method of installation is via\n``pip``.\n\n.. code-block:: console\n\n   $ pip install easyrepr\n\nFor more installation options, see the `Installation section in the User Guide`_.\n\n.. _available on PyPI: https://pypi.org/project/easyrepr/\n.. _Installation section in the User Guide:\n   https://easyrepr.readthedocs.io/en/latest/guide.html#installation\n\n\nDocumentation\n=============\n\nFor full documentation, check out `easyrepr on Read the Docs`_.\n\n* `User Guide`_\n* `API Reference`_\n\n.. _easyrepr on Read the Docs: https://easyrepr.readthedocs.io/en/latest/\n.. _User Guide: https://easyrepr.readthedocs.io/en/latest/guide.html\n.. _API Reference: https://easyrepr.readthedocs.io/en/latest/api.html\n\n\nContributing\n============\n\nIf you're interesting in contributing to easyrepr, or just want to learn more\nabout how the project is built or structured, please read our `CONTRIBUTING\nfile`_.\n\n.. _CONTRIBUTING file: CONTRIBUTING.rst\n\n\nLicense\n=======\n\nThe `MIT license`_ applies to all files in the easyrepr repository and source\ndistribution. See the `LICENSE file`_ for more info.\n\n.. _MIT license: https://choosealicense.com/licenses/mit/\n.. _LICENSE file: LICENSE.rst\n",
    'author': 'Chris Bouchard',
    'author_email': 'chris@upliftinglemma.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrisbouchard/easyrepr',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
