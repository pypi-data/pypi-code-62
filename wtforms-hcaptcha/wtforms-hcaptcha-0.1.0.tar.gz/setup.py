# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wtforms_hcaptcha']

package_data = \
{'': ['*']}

install_requires = \
['markupsafe>=1.1.1,<2.0.0', 'wtforms>=2.3.3,<3.0.0']

setup_kwargs = {
    'name': 'wtforms-hcaptcha',
    'version': '0.1.0',
    'description': 'Custom WTForms field that handles hCaptcha display and validation.',
    'long_description': '# WTForms hCaptcha\n\n> Custom WTForms field that handles [hCaptcha](https://www.hcaptcha.com/) display and validation.\n\n<a href="https://github.com/jake-walker/wtforms-hcaptcha/actions"><img alt="Build Status" src="https://img.shields.io/github/workflow/status/jake-walker/wtforms-hcaptcha/Main/master?style=flat-square"></a>\n<a href="https://pypi.org/project/wtforms-hcaptcha/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/wtforms-hcaptcha?style=flat-square"></a>\n<img alt="GitHub License" src="https://img.shields.io/github/license/jake-walker/wtforms-hcaptcha?style=flat-square">\n\n[hCaptcha](https://www.hcaptcha.com/) is a CAPTCHA service that \'protects user privacy, rewards websites, and helps companies get their data labelled\'. This helps to prevent spam on websites by adding a challenge to forms that are hard for computers to solve, but easy for humans to solve.\n\nI wanted to use hCaptcha in one of my projects and although there are already Python libraries for working with hCaptcha, I had already used the WTForms ecosystem in that project so I wanted a drop in solution and as there were none at the time, I decided to create my own.\n\nThis is a modified version of [`wtforms-recaptcha`](https://pypi.org/project/wtforms-recaptcha/) by [Artem Gluvchynsky](excieve@gmail.com) to work with hCaptcha.\n\n## Installation\n\nUse `pip` to install on all systems:\n\n```bash\npip install wtforms-hcaptcha\n```\n\n## Usage Example\n\nThis example creates an empty form with just a CAPTCHA field.\n\n```python\nfrom wtforms.form import Form\nfrom wtforms-recaptcha import HcaptchaField\n\n\nclass MyForm(Form):\n    captcha = HcaptchaField(site_key="YOUR_SITE_KEY_HERE", secret_key="YOUR_SECRET_KEY_HERE")\n\nform = MyForm(request.form)\n\nif form.validate():\n    print("You are not a robot!")\nelse:\n    print(form.errors["captcha"])\n```\n\n## Development Setup\n\nThis project uses Poetry to manage dependencies and packaging. [Here](https://python-poetry.org/docs/#installation) are the installation instructions for Poetry.\n\n## Contributing\n\n1. Fork it (https://github.com/jake-walker/wtforms-hcaptcha/fork)\n2. Create your feature branch (`git checkout -b feature/foobar`)\n3. Commit your changes (`git commit -am "Add some foobar"`)\n4. Push to the branch (`git push origin feature/foobar`)\n5. Create a new pull request\n',
    'author': 'Jake Walker',
    'author_email': 'hi@jakew.me',
    'maintainer': 'Jake Walker',
    'maintainer_email': 'hi@jakew.me',
    'url': 'https://github.com/jake-walker/wtforms-hcaptcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
