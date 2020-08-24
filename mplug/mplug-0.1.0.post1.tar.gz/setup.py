# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mplug']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.7,<4.0.0']

entry_points = \
{'console_scripts': ['mplug = mplug:run']}

setup_kwargs = {
    'name': 'mplug',
    'version': '0.1.0.post1',
    'description': 'A plugin manager for mpv',
    'long_description': 'MPlug – a Plugin Manager for MPV\n================================\n\nA plugin manager for mpv to easy install and uninstall mpv scripts and more.\n\nInstallation\n------------\n- Install dependencies: python3, GitPython\n- Clone this repository\n- Run with `run.py`\n\nUsage\n-----\n- To install a plugin `mplug install plugin_name`\n- To update all plugins: `mplug upgrade`\n- To upgrade database: `mplug update`\n- To uninstall a plugin: `mplug uninstall plugin_id`\n- To disable a plugin without uninstalling it: `mplug disable plugin_id`\n- To search for a plugin `mplug search term`\n- To list all installed plugins `mplug list-installed`\n- You can find plugins in the WebUI of the [mpv script directory](https://nudin.github.io/mpv-script-directory/)\n\nStatus & Todo\n-------------\n- [X] Populate mpv script directory, by scraping wiki\n- [X] First version of plugin manager\n- [X] Write a Webinterface to browse plugins\n- [ ] Add install instructions for all plugins to the [mpv script directory](https://github.com/Nudin/mpv-script-directory)\n- [ ] Write a TUI\n- [ ] Write a GUI\n',
    'author': 'Michael F. Schönitzer',
    'author_email': 'michael@schoenitzer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nudin/mplug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
