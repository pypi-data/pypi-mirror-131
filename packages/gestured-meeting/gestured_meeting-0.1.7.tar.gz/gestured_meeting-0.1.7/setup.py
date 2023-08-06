# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gestured_meeting', 'gestured_meeting.gesture', 'gestured_meeting.meeting']

package_data = \
{'': ['*'], 'gestured_meeting': ['icons/*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0',
 'PyAutoGUI>=0.9.53,<0.10.0',
 'bleak>=0.12.1,<0.13.0',
 'pystray>=0.17.3,<0.18.0']

extras_require = \
{':platform_system == "Linux"': ['PyGObject>=3.42.0,<4.0.0']}

entry_points = \
{'console_scripts': ['gestured-meeting = gestured_meeting:cli']}

setup_kwargs = {
    'name': 'gestured-meeting',
    'version': '0.1.7',
    'description': 'Online meeting with gesture.',
    'long_description': '<h1 align="center"><img src="https://raw.githubusercontent.com/ygkn/gestured-meeting/main/logo.svg" alt="Gestured Meeting" /></h1>\n\n<p align="center">\nOnline meeting with gesture.\n</p>\n\nLogo and icons are remixed [Heroicons](https://heroicons.com/) and [Twemoji](https://twemoji.twitter.com/).\n\n## Useage\n\n### Requirements\n\n- Python ^3.9\n\n#### Ubuntu / Debian\n\n```\nsudo apt install \\\n  libgirepository1.0-dev \\\n  gcc libcairo2-dev \\\n  pkg-config \\\n  python3-dev \\\n  gir1.2-gtk-3.0 \\\n  gir1.2-appindicator3-0.1\n```\n\nSee [Getting Started — PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html), [techgaun/nepali-calendar-indicator#5](https://github.com/techgaun/nepali-calendar-indicator/issues/5)\n\n### Supported OS\n\n#### Tested\n\n- Ubuntu 20.04\n\n### Untested\n\n- Windows\n- macOS\n- other Linux using GNOME or Xorg\n\n### Installation\n\n```\npip install gestured_meeting\n```\n\n### Start\n\n```\ngestured-meeting\n```\n\n**Note**: PyPI package is gestured_meeting, but command is gestured-meeting.\n\n### Graphical User Interface (System Tray)\n\n- **Watching** - watching Gestured Meeting your gesture\n- **Gesture Provider** - how to connect to your gesture device. now, supported BLE only\n- **Meeting Platform** - online meeting platform to operate\n- **Exit** - exit Gestured Meeting\n\n### Command-line Options\n\n- **`-h`, `--help`** - show this help message and exit\n- **`-r`, `--run`** - run on start (default is on, `--no-run` makes off it)\n- **`-m`, `--meeting`** - gesture provider (`zoom` or `meet`, default is `zoom`)\n- **`-g`, `--gesture`** - gesture provider (now allows `ble` only, default is `ble`)\n\n## Develop\n\n### Requirements\n\n- Python ^3.9\n- Poetry\n\n### Installation\n\n1. clone this repo.\n2. `poetry install`\n\n### Run\n\n```\npoetry run gestured-meeting\n```\n\n### Contribution\n\nContributions are welcome.\n',
    'author': 'ygkn',
    'author_email': '2000ygkn0713@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
