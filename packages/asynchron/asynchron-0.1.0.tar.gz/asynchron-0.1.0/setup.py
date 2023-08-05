# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asynchron',
 'asynchron.amqp',
 'asynchron.amqp.consumer',
 'asynchron.amqp.publisher',
 'asynchron.amqp.serializer',
 'asynchron.codegen',
 'asynchron.codegen.generator',
 'asynchron.codegen.generator.jinja',
 'asynchron.codegen.spec',
 'asynchron.codegen.spec.reader',
 'asynchron.codegen.spec.transformer',
 'asynchron.codegen.spec.viewer',
 'asynchron.codegen.spec.visitor',
 'asynchron.codegen.spec.walker',
 'asynchron.codegen.writer',
 'asynchron.core']

package_data = \
{'': ['*'],
 'asynchron.codegen.generator.jinja': ['templates/*', 'templates/base/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'aio-pika>=6.8.0,<7.0.0',
 'click>=8.0.3,<9.0.0',
 'dependency-injector>=4.37.0,<5.0.0',
 'jsonschema>=4.2.1,<5.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'stringcase>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['asynchron-codegen = asynchron.codegen:cli']}

setup_kwargs = {
    'name': 'asynchron',
    'version': '0.1.0',
    'description': 'Python service framework with code generator based on AsyncAPI specification',
    'long_description': '# asynchron\nPython service framework with code generator based on AsyncAPI specification\n',
    'author': 'zerlok',
    'author_email': 'denergytro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zerlok/asynchron',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
