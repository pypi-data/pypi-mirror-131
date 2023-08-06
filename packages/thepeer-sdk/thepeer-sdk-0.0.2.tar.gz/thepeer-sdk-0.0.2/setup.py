# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thepeer_sdk', 'thepeer_sdk.core', 'thepeer_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'thepeer-sdk',
    'version': '0.0.2',
    'description': 'Python SDK for Thepeer',
    'long_description': '# Thepeer Python SDK\n\n![GitHub issues](https://img.shields.io/github/issues/Emmarex/thepeer-sdk-python)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/thepeer-sdk)\n![PyPI](https://img.shields.io/pypi/v/thepeer-sdk)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/thepeer-sdk)\n![PyPI - License](https://img.shields.io/pypi/l/thepeer-sdk)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nPython SDK for [Thepeer](https://thepeer.co/).\n\n## Quick Start\n\n1. Install thepeer-sdk\n\n```bash\npip install thepeer-sdk\n```\n\n2. Signup to get your API keys [here](https://dashboard.thepeer.co/login)\n\n## Usage\n\n\n### Initiate\n```python\nfrom thepeer_sdk import ThepeerSdkClient\n\nthepeer_sdk_client = ThepeerSdkClient(\n    secret_key="SECRET_KEY_GOES_HERE"\n)\n\n# Get the list of all indexed users\nthepeer_sdk_client.list_users()\n```\n\n### Available Methods\n#### User\n- index_user\n    : Index a particular user on Thepeer\n\n    **parameters**:\n    - name(str)\n    - identifier(str)\n    : unique user identifier\n    - email(str)\n\n    **returns**: dict\n\n- list_users\n    : Get the list of all indexed users\n\n    **parameters**:\n    - page(int)\n    : page number to return\n    - perPage(int)\n    : amount of records to return per page\n\n    **returns**: dict\n\n- update_user\n    : Update your user\'s identifier when they make a profile update to their identifier on your platform.\n\n    **parameters**:\n    - user_ref(str)\n    : the reference returned when the user was indexed\n    - user_identifier(str)\n    : unique user identifier\n\n    **returns**: dict\n\n- delete_user\n    : Delete a user in the event that a user deactivates their account on your platform\n\n    **parameters**:\n    - user_ref(str)\n    : the reference returned when the user was indexed\n\n    **returns**: dict\n\n#### Link\n- get_user_links\n    : This returns all linked accounts associated with a user.\n\n    **parameters**:\n    - user_ref(str)\n    : the reference returned when the user was indexed\n\n    **returns**: dict\n\n- get_link\n    : Get a linked account details\n\n    **parameters**:\n    - link_id(str)\n    : link ID\n\n    **returns**: dict\n\n#### Send\n- verify_receipt\n    : Verify a particular receipt.\n\n    **parameters**:\n    - receipt_ref(str)\n    : reference of the receipt to process\n\n    **returns**: dict\n\n- process_receipt\n    : Process receipts generated from Thepeer inline.\n\n    **parameters**:\n    - receipt_ref(str)\n    : reference of the receipt to process\n    - event(str)\n\n    **returns**: dict\n\n#### Direct Charge\n- charge_link\n    : Charge your user\'s linked account at any time\n\n    **parameters**:\n    - link_id(str)\n    : id of the link to charge\n    - amount(int)\n    : amount to charge\n    - remark(str)\n    : narration of the charge\n\n    **returns**: dict\n\n- authorize_charge\n    : authorize direct charge request via webhooks\n\n    **parameters**:\n    - charge_ref(str)\n    : direct charge reference\n    - event(str)\n\n    **returns**: dict\n\n## Upgrade\n\n```bash\npip install --upgrade thepeer-sdk\n```\n\n## Extra\n\nVisit the official [Thepeer documentation](https://docs.thepeer.co/) for more information.\n\n\n## License\nSee LICENSE.\n',
    'author': 'Oluwafemi Tairu',
    'author_email': 'tairuoluwafemi09@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Emmarex/thepeer-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.12,<4.0.0',
}


setup(**setup_kwargs)
