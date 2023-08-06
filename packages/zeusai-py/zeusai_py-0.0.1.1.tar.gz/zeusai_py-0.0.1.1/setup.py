# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeusai_py', 'zeusai_py.io', 'zeusai_py.plugin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zeusai-py',
    'version': '0.0.1.1',
    'description': '',
    'long_description': '# ZeusAI.Py\nThe python package to wrap the various APIs associated with ZeusAI.\n\n## Usage for Non-Contributors\nSee the Readthedocs page (TODO) for usage documentation.\n\n## Documentation\nTo view all of the available documentation for this project, please see the [Documents Index](INDEX.md)\nThis includes information on getting started, the development environment, and more.\n\n## Version Numbers\nZeusAI.Py is updated at the same time as the ZeusAI server. The first 3 sections of the ZeusAI.Py version number will be the \nassociated version number for ZeusAI, with the 4th section being the ZeusAI.Py revision number, which is only updated for bugs.\n(i.e. if ZeusAI is on 1.2.3, ZeusAI.Py will be on 1.2.3.x).\n\nIf the first three sections of the ZeusAI.Py version number match your ZeusAI version number, they should be compatable.\n',
    'author': 'JMT',
    'author_email': 'contact@joshinshaker.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joshinshaker-tech/zeusai_py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
