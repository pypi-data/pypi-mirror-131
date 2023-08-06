# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyportable_installer',
 'pyportable_installer.checkup',
 'pyportable_installer.compilers',
 'pyportable_installer.compilers.lib.pyportable_runtime_py310.pyportable_runtime',
 'pyportable_installer.compilers.lib.pyportable_runtime_py38.pyportable_runtime',
 'pyportable_installer.compilers.lib.pyportable_runtime_py39.pyportable_runtime',
 'pyportable_installer.main_flow',
 'pyportable_installer.main_flow.step1',
 'pyportable_installer.main_flow.step2',
 'pyportable_installer.main_flow.step3',
 'pyportable_installer.main_flow.step3.step3_1',
 'pyportable_installer.main_flow.step3.step3_2',
 'pyportable_installer.main_flow.step3.step3_3',
 'pyportable_installer.main_flow.step3.step3_3.bat_2_exe',
 'pyportable_installer.main_flow.step4',
 'pyportable_installer.template.pylauncher']

package_data = \
{'': ['*'], 'pyportable_installer': ['template/*', 'template/depsland/*']}

install_requires = \
['embed-python-manager',
 'fire',
 'lk-logger',
 'lk-utils>=2.1.2',
 'pyportable-crypto>=1.0.0']

setup_kwargs = {
    'name': 'pyportable-installer',
    'version': '4.2.1',
    'description': 'Build and distribute portable Python application by all-in-one configuration file.',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
