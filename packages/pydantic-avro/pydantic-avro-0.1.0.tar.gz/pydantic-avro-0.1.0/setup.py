# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_avro']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.0.0']

entry_points = \
{'console_scripts': ['pydantic-avro = pydantic_avro.__main__:root_main']}

setup_kwargs = {
    'name': 'pydantic-avro',
    'version': '0.1.0',
    'description': 'Converting pydantic classes to avro schemas',
    'long_description': '# pydantic-avro\n\nThis library can convert a pydantic class to a avro schema or generate python code from a avro schema.\n\n### Install\n\n```bash\npip install pydantic-avro\n```\n\n### Pydantic class to avro schema\n\n```python\nimport json\nfrom typing import Optional\n\nfrom pydantic_avro.base import AvroBase\n\nclass TestModel(AvroBase):\n    key1: str\n    key2: int\n    key2: Optional[str]\n\nschema_dict: dict = TestModel.avro_schema()\nprint(json.dumps(schema_dict))\n\n```\n\n### Avro schema to pydantic\n\n```shell\n# Print to stdout\npydantic-avro avro_to_pydantic --asvc /path/to/schema.asvc\n\n# Save it to a file\npydantic-avro avro_to_pydantic --asvc /path/to/schema.asvc --output /path/to/output.py\n```\n\n\n### Install for developers\n\n###### Install package\n\n- Requirement: Poetry 1.*\n\n```shell\npoetry install\n```\n\n###### Run unit tests\n```shell\npytest\ncoverage run -m pytest  # with coverage\n# or (depends on your local env) \npoetry run pytest\npoetry run coverage run -m pytest  # with coverage\n```\n\n##### Run linting\n\nThe linting is checked in the github workflow. To fix and review issues run this:\n```shell\nblack .   # Auto fix all issues\nisort .   # Auto fix all issues\npflake .  # Only display issues, fixing is manual\n```\n',
    'author': "Peter van 't Hof'",
    'author_email': 'peter.vanthof@godatadriven.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/godatadriven/pydantic-avro',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
