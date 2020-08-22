# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hootsweet']

package_data = \
{'': ['*']}

install_requires = \
['cherrypy>=18.5.0,<19.0.0',
 'pytz>=2019.3,<2020.0',
 'requests>=2.23,<3.0',
 'requests_oauthlib>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'hootsweet',
    'version': '0.7.1',
    'description': 'A python library for the HootSuite REST API.',
    'long_description': '==========\nHootsweet\n==========\n\n.. image:: https://img.shields.io/pypi/v/hootsweet\n    :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/hootsweet\n    :alt: PyPI Versions\n\n.. image:: https://img.shields.io/pypi/format/hootsweet\n    :alt: PyPi Format\n\n.. image:: https://requires.io/github/ciaranmccormick/hootsweet/requirements.svg?branch=develop\n    :target: https://requires.io/github/ciaranmccormick/hootsweet/requirements/?branch=develop\n    :alt: Requirements Status\n\n.. image:: https://readthedocs.org/projects/hootsweet/badge/?version=latest\n    :target: https://hootsweet.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\nA python API for the HootSuite REST API.\n\n------------\nInstallation\n------------\n\n.. code-block:: shell\n\n    pip install hootsweet\n\n-----\nUsage\n-----\n\n.. code-block:: python\n\n    from hootsweet import HootSweet\n\n    client_id = "Your-HootSuite-Client-ID"\n    client_secret = "Your-HootSuite-Client-Secret"\n    redirect_uri = "http://redirect.uri/"\n\n    def handle_refresh(token):\n        # callback function to save token to a database or file\n        save_token_to_db(token)\n\n    client = HootSweet(client_id, client_secret, redirect_uri=redirect_uri, refresh_cb=handle_refresh)\n\n    # Step 1 get authorization url from HootSuite\n    url, state = client.authorization_url()\n\n    # Step 2 go to url above and get OAuth2 code\n    token = client.fetch_token(code)\n\n    # client.token now contains your authentication token\n    # Step 3 (optional) refresh token periodically, this automatically calls handle_refresh\n    token = client.refresh_token()\n\n    # retrieve data from https://platform.hootsuite.com/v1/me\n    me = client.get_me()\n\n    # retrieve authenticated members organizations https://platform.hootsuite.com/v1/me/organizations\n    organizations = client.get_me_organizations()\n\n\nMessages\n=========\n\n.. code-block:: python\n\n    token = {\n    "access_token": "e9a90a81-xf2d-dgh3-cfsd-23jhvn76",\n    "token_Type": "Bearer",\n    "expires_in": 2592000,\n    "refresh_token": "82d82cf4-76gf-gfds-nt3k-lzpo12jg",\n    "scope": "offline"\n    }\n\n    client = HootSweet("client_id", "client_secret", token=token)\n\n    # Schedule a message\n    text = "A message"\n    social_profile_ids = ["1234", "12345"]\n    send_time = datetime(2020, 1, 1, 12, 40, 15)\n    message = client.schedule_message(text=text, social_profile_ids=social_profile_ids,\n                                send_time=send_time)\n\n    # Get message\n    message = client.get_message(message_id="98765")\n\n    # Delete message\n    client.delete_message(message_id="98765")\n\n\nMessages with Media\n===================\n\nHootSuite uses it\'s own AWS Bucket to add media to a message. To\nattach media to you message you need to first upload the media\nto HootSuite\'s bucket.\n\n.. code-block:: python\n\n    token = {\n    "access_token": "e9a90a81-xf2d-dgh3-cfsd-23jhvn76",\n    "token_Type": "Bearer",\n    "expires_in": 2592000,\n    "refresh_token": "82d82cf4-76gf-gfds-nt3k-lzpo12jg",\n    "scope": "offline"\n    }\n\n    client = HootSweet("client_id", "client_secret", token=token)\n\n    mime_type = "image/png"\n    file_path = Path("/path/to/file.png")\n    file_size = file_path.stat().st_size\n    upload_details = client.create_media_upload_url(file_size, mime_type)\n    upload_url = upload_details["uploadUrl"]\n    media_id = upload_details["id"]\n\n    # The number of seconds you have to upload the media\n    expires_in = upload_details["uploadUrlDurationSeconds"]\n\n    # Upload the media\n    with file_path.open("rb") as f:\n        content = f.read()\n        headers = {"Content-Type": mime_type, "Content-Length": str(file_size)}\n        # Make sure that this request returns a 200\n        requests.put(upload_url, headers=headers, data=content)\n\n    # Schedule a message\n    text = "A message"\n    social_profile_ids = ["1234", "12345"]\n    send_time = datetime(2020, 1, 1, 12, 40, 15)\n    media = [{"id": media_id}]\n    message = client.schedule_message(text=text, social_profile_ids=social_profile_ids,\n                                  send_time=send_time, media=media)\n',
    'author': 'Ciaran McCormick',
    'author_email': 'ciaran@ciaranmccormick.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
