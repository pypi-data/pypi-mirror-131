# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sans_db', 'sans_db.template_backends']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-sans-db',
    'version': '0.1.0',
    'description': 'Tools to limit database access in parts of your Django codebase ',
    'long_description': '# Django sans DB\n\nTools for limiting access to the database in parts of your Django code.\n',
    'author': 'Charlie Denton',
    'author_email': 'charlie@meshy.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meshy/django-sans-db',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<3.11',
}


setup(**setup_kwargs)
