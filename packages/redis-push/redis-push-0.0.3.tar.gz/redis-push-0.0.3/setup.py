# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['redis_push', 'redis_push.model']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.0,<3.0.0', 'pydantic[dotenv]>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'redis-push',
    'version': '0.0.3',
    'description': 'push data into redis follow protocol.',
    'long_description': None,
    'author': 'agarichan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agarichan/redis-push',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
