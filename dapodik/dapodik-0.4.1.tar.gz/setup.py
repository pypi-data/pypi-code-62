# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dapodik',
 'dapodik.base',
 'dapodik.customrest',
 'dapodik.peserta_didik',
 'dapodik.ptk',
 'dapodik.rest',
 'dapodik.rombongan_belajar',
 'dapodik.sarpras',
 'dapodik.sekolah',
 'dapodik.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'lxml>=4.5.2,<5.0.0',
 'openpyxl>=3.0.4,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dapodik = dapodik.__main__:main']}

setup_kwargs = {
    'name': 'dapodik',
    'version': '0.4.1',
    'description': 'Client / API aplikasi Dapodik',
    'long_description': '# dapodik\n\n[![dapodik - PyPi](https://img.shields.io/pypi/v/dapodik)](https://pypi.org/project/dapodik/)\n[![Download](https://img.shields.io/badge/Download-Unduh-brightgreen)](https://github.com/hexatester/dapodik/archive/master.zip)\n[![Donate DANA](https://img.shields.io/badge/Donasi-DANA-blue)](https://link.dana.id/qr/1lw2r12r)\n[![Tutorial](https://img.shields.io/badge/Tutorial-Penggunaan-informational)](https://github.com/hexatester/dapodik/wiki)\n[![Group Telegram](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://t.me/dapodik_2021)\n[![codecov](https://codecov.io/gh/hexatester/dapodik/branch/master/graph/badge.svg)](https://codecov.io/gh/hexatester/dapodik)\n[![LISENSI](https://img.shields.io/github/license/hexatester/dapodik)](https://github.com/hexatester/dapodik/blob/master/LISENSI)\n[![BUILD](https://img.shields.io/travis/com/hexatester/dapodik)](https://travis-ci.com/github/hexatester/dapodik)\n\nPython client / API aplikasi dapodik.\n\n## Install\n\nPastikan [python 3.7](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe) terinstall,\nkemudian jalankan perintah di bawah dalam Command Prompt atau Powershell (di Windows + X):\n\n```bash\npip install --upgrade dapodik\n```\n\n## Release\n\nPerkiraan release versi 1 akhir bulan September 2020,\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh [Kemdikbud](https://kemdikbud.go.id/) atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. _Gunakan dengan risiko Anda sendiri._\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexatester/dapodik',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
