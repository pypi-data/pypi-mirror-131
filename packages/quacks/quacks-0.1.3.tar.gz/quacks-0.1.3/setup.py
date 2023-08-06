# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quacks']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>3.7,<5']

extras_require = \
{':python_version < "3.7"': ['dataclasses>0.4'],
 ':python_version < "3.8"': ['importlib-metadata>=1,<5']}

setup_kwargs = {
    'name': 'quacks',
    'version': '0.1.3',
    'description': 'Better duck-typing with mypy-compatible extensions to Protocol',
    'long_description': "🦆 Quacks\n=========\n\n.. image:: https://img.shields.io/pypi/v/quacks.svg\n   :target: https://pypi.python.org/pypi/quacks\n\n.. image:: https://img.shields.io/pypi/l/quacks.svg\n   :target: https://pypi.python.org/pypi/quacks\n\n.. image:: https://img.shields.io/pypi/pyversions/quacks.svg\n   :target: https://pypi.python.org/pypi/quacks\n\n.. image:: https://github.com/ariebovenberg/quacks/actions/workflows/build.yml/badge.svg\n   :target: https://github.com/ariebovenberg/quacks/actions/workflows/build.yml\n\n.. image:: https://img.shields.io/readthedocs/quacks.svg\n   :target: http://quacks.readthedocs.io/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\n.. epigraph::\n\n  If it walks like a duck and it quacks like a duck, then it must be a duck\n\n\nThanks to `PEP544 <https://www.python.org/dev/peps/pep-0544/>`_, Python now has protocols:\na way to define duck typing statically.\nThis library gives you some niceties to make common idioms easier.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n   pip install quacks\n\n⚠️ For type checking to work with ``mypy``, you'll need to enable the plugin in\nyour `mypy config file <https://mypy.readthedocs.io/en/latest/config_file.html>`_:\n\n.. code-block:: ini\n\n   [mypy]\n   plugins = quacks.mypy\n\nFeatures\n--------\n\nEasy read-only protocols\n^^^^^^^^^^^^^^^^^^^^^^^^\n\nDefining read-only protocols is great for encouraging immutability and\nworking with frozen dataclasses. Use the ``readonly`` decorator:\n\n\n.. code-block:: python\n\n    from quacks import readonly\n\n    @readonly\n    class User(Protocol):\n        id: int\n        name: str\n        is_premium: bool\n\nWithout this decorator, we'd have to write quite a lot of cruft,\nreducing readability:\n\n\n.. code-block:: python\n\n    class User(Protocol):\n        @property\n        def id(self) -> int: ...\n        @property\n        def name(self) -> str: ...\n        @property\n        def is_premium(self) -> bool: ...\n\nPartial protocols (work in progress)\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nWhat if you want to reuse parts of a protocol?\nImagine we have several functions who use various properties of ``User``.\nWith partial protocols you can reuse attributes without having to define\nmany overlapping protocols.\nInspired by `clojure spec <https://youtu.be/YR5WdGrpoug?t=1971>`_.\n\n(exact syntax TBD)\n\n.. code-block:: python\n\n    class User(Protocol):\n        id: int\n        name: str\n        is_premium: bool\n        address: Address\n\n    class Address(Protocol):\n        street: str\n        city: str\n        country: str\n\n    from quacks import _\n\n    def determine_discount(u: User[_.id.is_premium]) -> int:\n        ...  # access `id` and `is_premium` attributes\n\n    def greet(u: User[_.name.address[_.country]]) -> None:\n        ...  # access `name` and `address.country` attributes\n\n    u: User = ...\n\n    determine_discount(u)\n    greet(u)\n",
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ariebovenberg/quacks',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
