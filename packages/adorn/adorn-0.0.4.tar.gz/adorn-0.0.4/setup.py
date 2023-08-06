# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['adorn', 'adorn.data', 'adorn.exception', 'adorn.orchestrator', 'adorn.unit']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'adorn',
    'version': '0.0.4',
    'description': 'Adorn',
    'long_description': 'Adorn\n======\n\n|PyPI| |Status| |Python Version| |License|\n\n|Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/adorn.svg\n   :target: https://pypi.org/project/adorn/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/adorn.svg\n   :target: https://pypi.org/project/adorn/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/adorn\n   :target: https://pypi.org/project/adorn\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/adorn\n   :target: https://opensource.org/licenses/Apache-2.0\n   :alt: License\n.. |Tests| image:: https://github.com/pyadorn/adorn/workflows/Tests/badge.svg\n   :target: https://github.com/pyadorn/adorn/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/pyadorn/adorn/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/pyadorn/adorn\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n``adorn`` is a configuration tool for python code.\n\n``adorn`` can currently\n\n* instantiate an object\n* check that a config can instantiate an object\n\n\nExample\n-------\n\n.. code-block:: python\n\n   from collections import defaultdict\n\n\n   from adorn.orchestrator.base import Base\n   from adorn.params import Params\n   from adorn.unit.complex import Complex\n   from adorn.unit.constructor_value import ConstructorValue\n   from adorn.unit.parameter_value import ParameterValue\n   from adorn.unit.python import Python\n\n\n   class Example(Complex):\n       _registry = defaultdict(dict)\n       _subclass_registry = dict()\n       _intermediate_registry = defaultdict(list)\n       _parent_registry = defaultdict(list)\n\n\n   @Example.register(None)\n   class Parent(Example):\n       def __init__(self, parent_value: str) -> None:\n           super().__init__()\n           self.parent_value = parent_value\n\n\n   @Parent.register("child")\n   class Child(Parent):\n       def __init__(self, child_value: int, **kwargs) -> None:\n           super().__init__(**kwargs)\n           self.child_value = child_value\n\n\n   base = Base(\n       [\n           ConstructorValue(),\n           ParameterValue(),\n           Example(),\n           Python()\n       ]\n   )\n\n   params = Params(\n           {\n               "type": "child",\n               "child_value": 0,\n               "parent_value": "abc"\n           }\n   )\n\n   # well specified configuration\n   # we can type check from any level in the\n   # class hierarchy\n   assert base.type_check(Example, params) is None\n   assert base.type_check(Parent, params) is None\n   assert base.type_check(Child, params) is None\n\n   # instantiate\n   # we can instantiate from any level in the\n   # class hierarchy\n   example_obj = base.from_obj(\n       Example,\n       params\n   )\n\n   assert isinstance(example_obj, Child)\n\n\n   parent_obj = base.from_obj(\n       Parent,\n       params\n   )\n\n   assert isinstance(parent_obj, Child)\n\n\n   child_obj = base.from_obj(\n       Child,\n       params\n   )\n\n   assert isinstance(child_obj, Child)\n\n\n\nInstallation\n------------\n\nYou can install *Adorn* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install adorn\n\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `Apache 2.0 license`_,\n*Adorn* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _Apache 2.0 license: https://opensource.org/licenses/Apache-2.0\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/pyadorn/adorn/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://adorn.readthedocs.io/en/latest/usage.html\n',
    'author': 'Jacob Baumbach',
    'author_email': 'jacob.baumbach@hey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyadorn/adorn',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
