# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['blacksmith',
 'blacksmith.domain',
 'blacksmith.domain.model',
 'blacksmith.middleware',
 'blacksmith.sd',
 'blacksmith.sd.adapters',
 'blacksmith.service',
 'blacksmith.service.adapters']

package_data = \
{'': ['*']}

install_requires = \
['aiobreaker>=1.2.0,<2.0.0',
 'httpx>=0.21.1,<0.22.0',
 'pydantic>=1.8.2,<2.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

extras_require = \
{'prometheus': ['prometheus-client>=0.12.0,<0.13.0']}

setup_kwargs = {
    'name': 'blacksmith',
    'version': '0.5.0',
    'description': 'REST API Client designed for microservices',
    'long_description': 'Blacksmith\n==========\n\n.. image:: https://readthedocs.org/projects/python-blacksmith/badge/?version=latest\n   :target: https://python-blacksmith.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/mardiros/blacksmith/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/mardiros/blacksmith/actions/workflows/main.yml\n   :alt: Continuous Integration\n\n.. image:: https://codecov.io/gh/mardiros/blacksmith/branch/master/graph/badge.svg?token=17KAC0LW9H\n   :target: https://codecov.io/gh/mardiros/blacksmith\n   :alt: Coverage Report\n\n\nBlacksmith is a library to build a solid microservices architecture based on REST API.\n\nTodays, developers have lots of choices to create microservices,\nplenty of framework are available, but when it comes to consume them,\nthere is a lack of clients.\n\nConsuming an API, is not just about doing HTTP requests, it has to be designed\nfor failure, monitoring, and service discovery with an elegant abstraction.\nblacksmith aims to provide a solution for developers to write clean client code,\nand for ops to monitor api calls on the client side.\n\n\nWhat is Blacksmith\n------------------\n\nBlacksmith is a declarative tool for REST Api.\n\nIn a REST API, resources are declared under HTTP routes, and every http verb\nas its own definition.\n\nIn Blacksmith, every resources are bound to schemas that define request and response,\nin order abstract HTTP.\n\nThis is a common concept for SQL table with ORM, where tables are bound to models,\nand then, operations are available on models. This is a usefull abstraction to \nwrite maintainable code and to dive into a project easilly.\n\nHandling API resources using an http client, such as `requests`_ does not handle\nthat abstraction, and does not handle bindings to object, and can be compared to\na raw connection because it is just a transport.\n\nThis is the problem blacksmith is solving, having a nice abstraction of a service.\n\n.. note::\n\n   | Blacksmith is not an HTTP Client or a model validator.\n   | Blacksmith use `httpx`_ to perform http query, and use `Pydantic`_ to validate models.\n\n.. _`requests`: https://docs.python-requests.org/\n.. _`httpx`: https://www.python-httpx.org/\n.. _`Pydantic`: https://pydantic-docs.helpmanual.io/\n\n\nWhy not using a SDK to consume APIs ?\n-------------------------------------\n\nSDK are about importing an external library in a service. And a service is\nconsumed by many services for different purpose. As a result, SDK create\ncoupling between service, and this is something that should be avoid.\n\nAn SDK for a service will declare all the resources, routes, and attribute\nof resources when a service consumer may consume just a few.\n\nSDK may hide what is really used by every service.\n\nTo avoid this, every consumers of API, should declare its own consumers\ncontracts to get a better view of which service use what.\n\n.. note::\n\n   TLDR; SDK are fine in public API, by the way, but not in a microservices\n   architecture.\n\n\nBuilding SDK\n------------\n\nBy the way, public API provider comes with an SDK, which is a good case,\nand blacksmith can be used to build SDK for Python / asyncio. \n\n\nRead More\n---------\n\nYou can read the `full documentation of this library here`_.\n\n.. _`full documentation of this library here`: https://blacksmith.readthedocs.io/en/latest/user/index.html\n\n\nContributing\n------------\n\n * Use isort and black to keep the code well formatted.\n * Write tests (Test driven development is encouraged).\n * Using just_ to run commands.\n\n.. _just: https://github.com/casey/just\n',
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mardiros/blacksmith',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
