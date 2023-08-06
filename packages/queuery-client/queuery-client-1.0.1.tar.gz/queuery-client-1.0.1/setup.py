# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['queuery_client']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{'pandas': ['pandas>=1.2.3,<2.0.0']}

setup_kwargs = {
    'name': 'queuery-client',
    'version': '1.0.1',
    'description': 'Queuery Redshift HTTP API Client for Python',
    'long_description': '# queuery_client_python\n\nQueuery Redshift HTTP API Client for Python\n\n## Installation\n\n`pip install queuery-client`\n\n## Usage\n\n- (a) naive iteration\n\n```python\nfrom queuery_client import QueueryClient\n\nclient = QueueryClient(endpoint="https://queuery.example.com")\nresponse = client.run("select column_a, column_b from the_great_table")\n\n# (a) iterate `response` naively\nfor elems in response:\n    print(response)\n\n# (b) invoke `read()` to fetch all records\nprint(response.read())\n\n# (c) invoke `read()` with `use_pandas=True` (returns `pandas.DataFrame`)\nprint(response.read(use_pandas=True))\n```\n',
    'author': 'altescy',
    'author_email': 'yasuhiro-yamaguchi@cookpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricolages/queuery_client_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
