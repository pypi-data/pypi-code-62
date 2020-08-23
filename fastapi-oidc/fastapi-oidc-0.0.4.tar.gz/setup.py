# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_oidc']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.1.1,<5.0.0',
 'fastapi>=0.61.0,<0.62.0',
 'pydantic>=1.6.1,<2.0.0',
 'python-jose[cryptography]>=3.2.0,<4.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'fastapi-oidc',
    'version': '0.0.4',
    'description': 'WIP | COMING SOON A simple library for parsing and verifying externally issued OIDC ID tokens in fastapi.',
    'long_description': '# fastapi OIDC WIP | COMING SOON\n\nVerify and decrypt 3rd party OIDC ID tokens to protect your [fastapi](https://github.com/tiangolo/fastapi) endpoints.\n\nReadTheDocs:\n\nSource code: [github](https://github.com/HarryMWinters/fastapi-oidc)\n\n## Table of Contents\n\n- Quick start\n- Troubleshooting\n- ReadTheDocs\n- Example\n\n### Quick Start\n\n`pip install fastapi-oidc`\n\n#### Verify ID Tokens Issued by Third Party\n\nThis is great if you just want to use something like Okta or google to handle\nyour auth. All you need to do is verify the token and then you can extract user\nID info from it.\n\n```python3\nfrom fastapi import Depends\nfrom fastapi import FastAPI\n\n# Set up our OIDC\nfrom fastapi_oidc import IDToken\nfrom fastapi_oidc import get_auth\n\nOIDC_config = {\n    "client_id": "",\n    "base_authorization_server_uri": "",\n    "issuer": "",\n    "signature_cache_ttl": int,\n}\n\nauthenticate_user: Callable = get_auth(**OIDC_config)\n\napp = FastAPI()\n\n@app.get("/protected")\ndef protected(id_token: IDToken = Depends(authenticate_user)):\n    return {"Hello": "World", "user_email": id_token.email}\n```\n',
    'author': 'HarryMWinters',
    'author_email': 'harrymcwinters@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HarryMWinters/fastapi-oidc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
