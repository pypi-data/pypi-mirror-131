# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['anshitsu']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'colorcorrect>=0.9.1,<0.10.0',
 'fire>=0.4.0,<0.5.0',
 'numpy>=1.21.0,<2.0.0']

entry_points = \
{'console_scripts': ['anshitsu = anshitsu.cli:main']}

setup_kwargs = {
    'name': 'anshitsu',
    'version': '1.0.1',
    'description': 'A tiny digital photographic utility.',
    'long_description': '# Anshitsu\n\n[![Testing](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml/badge.svg)](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml)\n\n[![codecov](https://codecov.io/gh/huideyeren/anshitsu/branch/main/graph/badge.svg?token=ZYRX8NBTLQ)](https://codecov.io/gh/huideyeren/anshitsu)\n\nA tiny digital photographic utility.\n\n"Anshitsu" means a darkroom in Japanese.\n\n## Usage\n\n```\nINFO: Showing help with the command \'anshitsu -- --help\'.\n\nNAME\n    anshitsu - Process Runnner for Command Line Interface\n\nSYNOPSIS\n    anshitsu PATH <flags>\n\nDESCRIPTION\n    This utility converts the colors of images such as photos.\n\n    If you specify a directory path, it will convert\n    the image files in the specified directory.\n    If you specify a file path, it will convert the specified file.\n    If you specify an option, the specified conversion will be performed.\n    \n    Tosaka mode is a mode that expresses the preference of\n    Tosaka-senpai, a character in "Kyūkyoku Chōjin R",\n    for "photos taken with Tri-X that look like they were\n    burned onto No. 4 or No. 5 photographic paper".\n    Only use floating-point numbers when using this mode;\n    numbers around 2.4 will make it look right.\n\nPOSITIONAL ARGUMENTS\n    PATH\n        Type: str\n        Directory or File Path\n\nFLAGS\n    --colorautoadjust=COLORAUTOADJUST\n        Type: bool\n        Default: False\n        Use colorautoadjust algorithm. Defaults to False.\n    --colorstretch=COLORSTRETCH\n        Type: bool\n        Default: False\n        Use colorstretch algorithm. Defaults to False.\n    --grayscale=GRAYSCALE\n        Type: bool\n        Default: False\n        Convert to grayscale. Defaults to False.\n    --negative=NEGATIVE\n        Type: bool\n        Default: False\n        Invert color. Defaults to False.\n    --tosaka=TOSAKA\n        Type: Optional[typing.Un...\n        Default: None\n        Use Tosaka mode. Defaults to None.\n\nNOTES\n    You can also use flags syntax for POSITIONAL ARGUMENTS\n```\n',
    'author': 'Iosif Takakura',
    'author_email': 'iosif@huideyeren.info',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/huideyeren',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
