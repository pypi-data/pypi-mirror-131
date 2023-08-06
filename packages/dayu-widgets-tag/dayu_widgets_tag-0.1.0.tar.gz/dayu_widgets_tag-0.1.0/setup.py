# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dayu_widgets_tag']

package_data = \
{'': ['*']}

install_requires = \
['QtPy>=1.11.3,<2.0.0', 'dayu_widgets>=0.9,<0.10']

setup_kwargs = {
    'name': 'dayu-widgets-tag',
    'version': '0.1.0',
    'description': 'Tag component for dayu_widgets as a plugin',
    'long_description': '# dayu_widgets_tag\n![](docs/_media/logo.svg)\n\nTag component is a dayu_widgets plugin\n\nSee the document:\n* [中文](https://muyr.github.io/dayu_widgets_tag/#/zh-cn/)\n* [EN](https://muyr.github.io/dayu_widgets_tag/)\n\n## Install\n```pip install dayu_widgets_tag```\n\n## Basic\n![](docs/_media/basic.png)\n\n## Preset Color\n![](docs/_media/preset-color.png)\n\n## Custom Color\n![](docs/_media/custom-color.png)\n\n## Checkable\n![](docs/_media/tag_checkable_light.gif)\n\n## Add and Delete\n![](docs/_media/tag_add_delete_light.gif)\n\n',
    'author': 'Yanru Mu ',
    'author_email': 'muyanru345@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/muyr/dayu_widgets_tag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
