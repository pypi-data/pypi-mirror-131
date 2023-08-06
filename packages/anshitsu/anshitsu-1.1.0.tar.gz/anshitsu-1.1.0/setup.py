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
    'version': '1.1.0',
    'description': 'A tiny digital photographic utility.',
    'long_description': '# Anshitsu\n\n[![Testing](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml/badge.svg)](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml)\n\n[![codecov](https://codecov.io/gh/huideyeren/anshitsu/branch/main/graph/badge.svg?token=ZYRX8NBTLQ)](https://codecov.io/gh/huideyeren/anshitsu)\n\nA tiny digital photographic utility.\n\n"Anshitsu" means a darkroom in Japanese.\n\n## Usage\n\n```\nINFO: Showing help with the command \'anshitsu -- --help\'.\n\nNAME\n    anshitsu - Process Runnner for Command Line Interface\n\nSYNOPSIS\n    anshitsu PATH <flags>\n\nDESCRIPTION\n    This utility converts the colors of images such as photos.\n\n    If you specify a directory path, it will convert\n    the image files in the specified directory.\n    If you specify a file path, it will convert the specified file.\n    If you specify an option, the specified conversion will be performed.\n\n    Tosaka mode is a mode that expresses the preference of\n    Tosaka-senpai, a character in "Kyūkyoku Chōjin R",\n    for "photos taken with Tri-X that look like they were\n    burned onto No. 4 or No. 5 photographic paper".\n    Only use floating-point numbers when using this mode;\n    numbers around 2.4 will make it look right.\n\nPOSITIONAL ARGUMENTS\n    PATH\n        Type: str\n        Directory or File Path\n\nFLAGS\n    --colorautoadjust=COLORAUTOADJUST\n        Type: bool\n        Default: False\n        Use colorautoadjust algorithm. Defaults to False.\n    --colorstretch=COLORSTRETCH\n        Type: bool\n        Default: False\n        Use colorstretch algorithm. Defaults to False.\n    --grayscale=GRAYSCALE\n        Type: bool\n        Default: False\n        Convert to grayscale. Defaults to False.\n    --invert=INVERT\n        Type: bool\n        Default: False\n        Invert color. Defaults to False.\n    --tosaka=TOSAKA\n        Type: Optional[typing.Un...\n        Default: None\n        Use Tosaka mode. Defaults to None.\n\nNOTES\n    You can also use flags syntax for POSITIONAL ARGUMENTS\n```\n\n\n\n## Algorithm\n\n### RGBA to RGB Convert\n\nConverts an image that contains Alpha, such as RGBA, to image data that does not contain Alpha.\nTransparent areas will be filled with white.\n\n### invert\n\nColor inversion by pillow.\n\n### colorautoajust\n\nUsing "automatic color equalization" algorithm.\n\n(References)\n\nA. Rizzi, C. Gatta and D. Marini, "A new algorithm for unsupervised global and local color correction.", Pattern Recognition Letters, vol. 24, no. 11, 2003.\n\n### colorstretch\n\nUsing "stretch" algorithm after "gray world" algorithm.\n\n(References)\n\nD. Nikitenko, M. Wirth and K. Trudel, "Applicability Of White-Balancing Algorithms to Restoring Faded Colour Slides: An Empirical Evaluation.", Journal of Multimedia, vol. 3, no. 5, 2008.\n\n### grayscale\n\nI implemented it based on the method described in this article.\n\n[Python でグレースケール(grayscale)化](https://qiita.com/yoya/items/dba7c40b31f832e9bc2a#pilpillow-%E3%81%A7%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB%E5%8C%96-numpy-%E3%81%A7%E4%BD%8E%E8%BC%9D%E5%BA%A6%E5%AF%BE%E5%BF%9C)\n\nNote: This article is written in Japanese.\n\n### Tosaka mode\n\nTosaka mode is a mode that expresses the preference of Tosaka-senpai, a character in "Kyūkyoku Chōjin R", for "photos taken with Tri-X that look like they were burned onto No. 4 or No. 5 photographic paper".\n\nOnly use floating-point numbers when using this mode; numbers around 2.4 will make it look right.\n\nWhen this mode is specified, color images will also be converted to grayscale.\n\n## Special Thanks\n\nWe are using the following libraries.\n\n[shunsukeaihara/colorcorrect](https://github.com/shunsukeaihara/colorcorrect)\n',
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
