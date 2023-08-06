# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rmrk_tools', 'rmrk_tools.rmrk1_0_0', 'rmrk_tools.rmrk2_0_0']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-rmrk-tools',
    'version': '0.1.0a6',
    'description': 'Python port of Typescript rmrk-tools.',
    'long_description': 'py-rmrk-tools\n=============\n\nA port of [rmrk-tools](https://github.com/rmrk-team/rmrk-tools) for Python.\n\nInstallation\n------------\n\nPython 3.9 and higher supported.\n\n```console\npip install py-rmrk-tools\n```\n\nToDo\n----\n\n- [ ] Entities definition\n    - [x] NFT\n    - [ ] Collection\n- [ ] CLI\n- [ ] Consolidator\n- [ ] RemarkListener\n- [ ] fetchRemarks\n- [ ] IPFS helpers\n- [ ] Validation\n',
    'author': 'Alisher A. Khassanov',
    'author_email': 'a.khssnv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khssnv/py-rmrk-tools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
