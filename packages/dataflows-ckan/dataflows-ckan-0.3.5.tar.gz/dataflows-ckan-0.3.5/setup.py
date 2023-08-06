# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataflows_ckan', 'dataflows_ckan.processors']

package_data = \
{'': ['*']}

install_requires = \
['ckan-datapackage-tools>=0.1.0,<0.2.0',
 'dataflows>=0.3.3,<0.4.0',
 'datapackage>=1.15.2,<2.0.0',
 'tableschema-ckan-datastore>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'dataflows-ckan',
    'version': '0.3.5',
    'description': 'CKAN integration for Dataflows.',
    'long_description': "# dataflows-ckan\n\nDataflows processors to work with CKAN.\n\n## Features\n\n- `dump_to_ckan` processor\n\n## Contents\n\n<!--TOC-->\n\n  - [Getting Started](#getting-started)\n    - [Installation](#installation)\n    - [Examples](#examples)\n  - [Documentation](#documentation)\n    - [dump_to_s3](#dump_to_s3)\n  - [Contributing](#contributing)\n  - [Changelog](#changelog)\n\n<!--TOC-->\n\n## Getting Started\n\n### Installation\n\nThe package use semantic versioning. It means that major versions  could include breaking changes. It's recommended to specify `package` version range in your `setup/requirements` file e.g. `package>=1.0,<2.0`.\n\n```bash\n$ pip install dataflows-ckan\n```\n\n### Examples\n\nThese processors have to be used as a part of data flow. For example:\n\n```python\nflow = Flow(\n    load('data/data.csv'),\n    dump_to_ckan(\n        host,\n        api_key,\n        owner_org,\n        overwrite_existing_data=True,\n        push_to_datastore=False,\n        push_to_datastore_method='insert',\n        **options,\n    ),\n)\nflow.process()\n```\n\n## Documentation\n\n### dump_to_ckan\n\nSaves the DataPackage to a CKAN instance.\n\n## Contributing\n\nCreate a virtual environment and install [Poetry](https://python-poetry.org/).\n\nThen install the package in editable mode:\n\n```\n$ make install\n```\n\nRun the tests:\n\n```\n$ make test\n```\n\nFormat your code:\n\n```\n$ make format\n```\n\n## Changelog\n\n### 0.2.0\n\n- Full port to dataflows, and some refactoring, with a basic integration test.\n\n#### 0.1.0\n\n- an initial port from https://github.com/frictionlessdata/datapackage-pipelines-ckan based on the great work of @brew and @amercader\n",
    'author': 'Paul Walsh',
    'author_email': 'paul@walsh.co.il',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
