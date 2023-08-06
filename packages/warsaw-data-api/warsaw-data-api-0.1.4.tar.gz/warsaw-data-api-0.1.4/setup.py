# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['warsaw_data_api', 'warsaw_data_api.tests', 'warsaw_data_api.ztm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'warsaw-data-api',
    'version': '0.1.4',
    'description': 'Warsaw data python api',
    'long_description': '# Pythonic way to use Warsaw data API\n\nThis package allow to fetch data from API provided by "UM Warszawa" - https://api.um.warszawa.pl/\n\n## Getting Started\n\n### Installation\n\n```\npip install warsaw-data-api\n```\n\n### Using ZTM module\n\nWe can fetch all location data for buses:\n\n```\nimport warsaw_data_api\n\nztm = warsaw_data_api.client(\'ztm\', apikey=\'your_api_key\')\nbuses = ztm.get_buses_location()\n\nfor bus in buses:\n    print(bus)\n```\n\nWe can do the same for trams, as a parameter we can set number of tram line\n\n```\nimport warsaw_data_api\n\nztm = warsaw_data_api.client(\'ztm\', apikey=\'your_api_key\')\ntrams = ztm.get_trams_location(line=17)\n\nfor tram in trams:\n    print(tram)\n```\n\n### Passing API Key\n\nWe can pass API Key in two different ways:\n\n1. Pass API Key to client function as a parameter `ztm = warsaw_data_api.client(\'ztm\', apikey=\'your_api_key\')`\n2. Create environment variable called `WARSAW_DATA_API_KEY`\n',
    'author': 'Radoslaw Wielonski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
