# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kittycad',
 'kittycad.api',
 'kittycad.api.file',
 'kittycad.api.meta',
 'kittycad.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<22.0.0',
 'httpx>=0.15.4,<0.21.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'kittycad',
    'version': '0.0.5',
    'description': 'A client library for accessing KittyCAD',
    'long_description': '# kittycad.py\n\nThe Python API client for KittyCAD.\n\nThis is generated from\n[openapi-generators/openapi-python-client](https://github.com/openapi-generators/openapi-python-client).\n\n- [PyPI](https://pypi.org/project/kittycad/)\n- [Python docs](https://python.api.docs.kittycad.io/)\n- [KittyCAD API Docs](https://docs.kittycad.io/?lang=python)\n\n## Generating\n\nYou can trigger a build with the GitHub action to generate the client. This will\nautomatically update the client to the latest version based on the spec hosted\nat [api.kittycad.io](https://api.kittycad.io/).\n\nAlternatively, if you wish to generate the client locally, make sure you have\n[Docker installed](https://docs.docker.com/get-docker/) and run:\n\n```bash\n$ make generate\n```\n\n## Contributing\n\nPlease do not change the code directly since it is generated. PRs that change\nthe code directly will be automatically closed by a bot.\n\n## Usage\nFirst, create an authenticated client:\n\n```python\nfrom kittycad import AuthenticatedClient\n\nclient = AuthenticatedClient(token="your_token")\n```\n\nIf you want to use the environment variable `KITTYCAD_API_TOKEN` to do\nauthentication and not pass one to the client, do the following:\n\n```python\nfrom kittycad import AuthenticatedClientFromEnv\n\nclient = AuthenticatedClientFromEnv()\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom kittycad.models import AuthSession\nfrom kittycad.api.meta import meta_debug_session\nfrom kittycad.types import Response\n\nsession: AuthSession = meta_debug_session.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[AuthSession] = meta_debug_session.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom kittycad.models import AuthSession\nfrom kittycad.api.meta import meta_debug_session\nfrom kittycad.types import Response\n\nsession: AuthSession = await meta_debug_session.asyncio(client=client)\nresponse: Response[AuthSession] = await meta_debug_session.asyncio_detailed(client=client)\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
