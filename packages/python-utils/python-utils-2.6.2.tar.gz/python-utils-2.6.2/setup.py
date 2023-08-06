# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_utils']

package_data = \
{'': ['*']}

install_requires = \
['six']

extras_require = \
{'docs': ['mock', 'python-utils', 'sphinx'],
 'tests': ['flake8',
           'mock',
           'pytest',
           'pytest-cov',
           'pytest-flake8',
           'python-utils',
           'sphinx']}

setup_kwargs = {
    'name': 'python-utils',
    'version': '2.6.2',
    'description': 'Python Utils is a module with some convenient utilities not included with the standard Python install',
    'long_description': "Useful Python Utils\n==============================================================================\n\n.. image:: https://travis-ci.org/WoLpH/python-utils.svg?branch=master\n  :target: https://travis-ci.org/WoLpH/python-utils\n\n.. image:: https://coveralls.io/repos/WoLpH/python-utils/badge.svg?branch=master\n  :target: https://coveralls.io/r/WoLpH/python-utils?branch=master\n\nPython Utils is a collection of small Python functions and\nclasses which make common patterns shorter and easier. It is by no means a\ncomplete collection but it has served me quite a bit in the past and I will\nkeep extending it.\n\nOne of the libraries using Python Utils is Django Utils.\n\nDocumentation is available at: https://python-utils.readthedocs.org/en/latest/\n\nLinks\n-----\n\n - The source: https://github.com/WoLpH/python-utils\n - Project page: https://pypi.python.org/pypi/python-utils\n - Reporting bugs: https://github.com/WoLpH/python-utils/issues\n - Documentation: https://python-utils.readthedocs.io/en/latest/\n - My blog: https://wol.ph/\n\nRequirements for installing:\n------------------------------------------------------------------------------\n\n - `six` any recent version\n\nInstallation:\n------------------------------------------------------------------------------\n\nThe package can be installed through `pip` (this is the recommended method):\n\n    pip install python-utils\n    \nOr if `pip` is not available, `easy_install` should work as well:\n\n    easy_install python-utils\n    \nOr download the latest release from Pypi (https://pypi.python.org/pypi/python-utils) or Github.\n\nNote that the releases on Pypi are signed with my GPG key (https://pgp.mit.edu/pks/lookup?op=vindex&search=0xE81444E9CE1F695D) and can be checked using GPG:\n\n     gpg --verify python-utils-<version>.tar.gz.asc python-utils-<version>.tar.gz\n\nQuickstart\n------------------------------------------------------------------------------\n\nThis module makes it easy to execute common tasks in Python scripts such as\nconverting text to numbers and making sure a string is in unicode or bytes\nformat.\n\nExamples\n------------------------------------------------------------------------------\n\nTo extract a number from nearly every string:\n\n.. code-block:: python\n\n    from python_utils import converters\n\n    number = converters.to_int('spam15eggs')\n    assert number == 15\n\n    number = converters.to_int('spam')\n    assert number == 0\n\n    number = converters.to_int('spam', default=1)\n    assert number == 1\n\n    number = converters.to_float('spam1.234')\n\nTo do a global import programmatically you can use the `import_global`\nfunction. This effectively emulates a `from ... import *`\n\n.. code-block:: python\n\n    from python_utils.import_ import import_global\n\n    # The following is  the equivalent of `from some_module import *`\n    import_global('some_module')\n\nOr add a correclty named logger to your classes which can be easily accessed:\n\n.. code-block:: python\n\n    class MyClass(Logged):\n        def __init__(self):\n            Logged.__init__(self)\n\n    my_class = MyClass()\n\n    # Accessing the logging method:\n    my_class.error('error')\n\n    # With formatting:\n    my_class.error('The logger supports %(formatting)s',\n                   formatting='named parameters')\n\n    # Or to access the actual log function (overwriting the log formatting can\n    # be done n the log method)\n    import logging\n    my_class.log(logging.ERROR, 'log')\n\n",
    'author': 'Rick van Hattem',
    'author_email': 'Wolph@wol.ph',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WoLpH/python-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
}


setup(**setup_kwargs)
