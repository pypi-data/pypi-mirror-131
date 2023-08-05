# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydrinker_gcp']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-pubsub>=2.8.0,<3.0.0', 'pydrinker>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pydrinker-gcp',
    'version': '1.1.2',
    'description': "Google Cloud Platform 'plugin' for pydrinker",
    'long_description': '# pydrinker-gcp\n![build on github actions](https://github.com/pydrinker/pydrinker-gcp/actions/workflows/test.yml/badge.svg?branch=main)\n\nThis is a extension of pydrinker for Google Cloud Provider to make pydrinker consume messages from [GCP Subscribers](https://cloud.google.com/pubsub/docs/subscriber).\n\nTo understand more about pydrinker [see org page](https://github.com/pydrinker).\n',
    'author': 'Rafael Henrique da Silva Correia',
    'author_email': 'rafael@abraseucodigo.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafaelhenrique/pydrinker-gcp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
