# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starknet',
 'starknet.net',
 'starknet.net.account',
 'starknet.utils',
 'starknet.utils.compiler',
 'starknet.utils.crypto',
 'starknet.utils.data_transformer',
 'starknet.utils.sync']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.4.1,<4.0.0', 'cairo-lang>=0.6.0,<0.7.0']

extras_require = \
{'docs': ['sphinx>=4.3.1,<5.0.0']}

setup_kwargs = {
    'name': 'starknet.py',
    'version': '0.1.0a0',
    'description': '',
    'long_description': '<h1 align="center">✨🐍 starknet.py</h1>\n<h2 align="center">StarkNet SDK for Python</h2>\n\n<p align="center">\n\n[![codecov](https://codecov.io/gh/software-mansion/starknet.py/branch/master/graph/badge.svg?token=3E54E8RYSL)](https://codecov.io/gh/software-mansion/starknet.py)\n<a href="https://github.com/software-mansion/starknet.py/actions">\n    <img src="https://img.shields.io/github/workflow/status/software-mansion/starknet.py/format -> lint -> test">\n</a>\n[![Documentation Status](https://readthedocs.org/projects/starknetpy/badge/?version=latest)](https://starknetpy.readthedocs.io/en/latest/?badge=latest)\n<a href="https://github.com/software-mansion/starknet.py/blob/main/LICENSE/">\n    <img src="https://img.shields.io/badge/license-MIT-black">\n</a>\n<a href="https://github.com/software-mansion/starknet.py/stargazers">\n    <img src=\'https://img.shields.io/github/stars/software-mansion/starknet.py?color=yellow\' />\n</a>\n<a href="https://starkware.co/">\n    <img src="https://img.shields.io/badge/powered_by-StarkWare-navy">\n</a>\n\n</p>\n\n## 📘 Documentation\n- [Installation](https://starknetpy.rtfd.io/en/latest/installation.html)\n- [Quickstart](https://starknetpy.rtfd.io/en/latest/quickstart.html)\n- [Guide](https://starknetpy.rtfd.io/en/latest/guide.html)\n- [API](https://starknetpy.rtfd.io/en/latest/api.html)\n\n## ▶️ Example usage\n### Asynchronous API\nThis is the recommended way of using the SDK.\n```\nfrom starknet.contract import Contract\nfrom starknet.net.client import Client\n\nkey = 1234\ncontract = await Contract.from_address("0x01336fa7c870a7403aced14dda865b75f29113230ed84e3a661f7af70fe83e7b", Client("testnet"))\ninvocation = await contract.functions["set_value"].invoke(key, 7)\nawait invocation.wait_for_acceptance()\n\n(saved,) = await contract.functions["get_value"].call(key) # (7)\n```\n\n### Synchronous API\nYou can access synchronous world with `_sync` postfix.\n\n```\nfrom starknet.contract import Contract\nfrom starknet.net.client import Client\n\nkey = 1234\ncontract = Contract.from_address_sync("0x01336fa7c870a7403aced14dda865b75f29113230ed84e3a661f7af70fe83e7b", Client("testnet"))\ninvocation = contract.functions["set_value"].invoke_sync(key, 7)\ninvocation.wait_for_acceptance_sync()\n\n(saved,) = contract.functions["get_value"].call_sync(key) # 7\n```\n\nSee more [here](https://starknetpy.rtfd.io/en/latest/quickstart.html).',
    'author': 'Tomasz Rejowski',
    'author_email': 'tomasz.rejowski@swmansion.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/software-mansion/starknet_python_sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.12,<4.0.0',
}


setup(**setup_kwargs)
