# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aggexif']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['aggexif = aggexif.main:main',
                     'sqlite = aggexif.sqlite_cache:main']}

setup_kwargs = {
    'name': 'aggexif',
    'version': '0.3.0',
    'description': "Aggregate Image's EXIF Tool",
    'long_description': '## Required\n- python 3.8 later & pip\n- exiftool\n\n## Install\n```\n# pip install aggexif\n```\n\n## Usage\n```\n$ aggexif ~/dir/*.NEF\n---- CAMERA LIST ----\nNIKON Z 7: 276▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\nNIKON Z 6: 69▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\n---- LENS LIST ----\nAF-S VR Zoom-Nikkor 70-300mm f/4.5-5.6G IF-ED: 213▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\n                       NIKKOR Z 14-30mm f/4 S: 69▇▇▇▇▇▇▇▇\n                        NIKKOR Z 50mm f/1.8 S: 48▇▇▇▇▇\n       AF-S Zoom-Nikkor 80-200mm f/2.8D IF-ED: 13\n---- FOCAL LENGTH ----\n  10-15: 19▇▇▇▇▇▇▇▇▇▇▇\n  15-20: 7▇▇▇\n  20-24: 9▇▇▇▇▇\n  28-35: 34▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\n  45-50: 48▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\n  60-70: 54▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\n  70-85: 30▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\n 85-105: 13▇▇▇▇▇▇▇\n105-135: 11▇▇▇▇▇\n135-200: 18▇▇▇▇▇▇▇▇▇▇\n200-300: 100▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\n```\n\n## Help\n```\n$ aggexif -h\nusage: Aggregate EXIF [-h] [-w WIDTH] [-l [LENS ...]] [-c [CAMERA ...]] [-a]\n                      [--ignore-cache]\n                      [paths ...]\n\npositional arguments:\n  paths                 images paths\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -w WIDTH, --width WIDTH\n                        print width\n  -l [LENS ...], --lens [LENS ...]\n                        select lens\n  -c [CAMERA ...], --camera [CAMERA ...]\n                        select camera\n  -a, --cache           save exif in cache\n  --ignore-cache        ignore cache\n```\n\n## Cache\nAggexif supports local caching. If you want to save the cache, add a --cache option. If you want to disable the cache temporarily, use a --ignore-cache option. Since the cache is stored in `~/.config/aggexif/exif.db as a SQLite, so you can delete it to remove all the cache.\n\n## Tested Camera\n- Nikon Z6/Z7(+FTZ)\n- SONY A7C/A7III\n- OLYMPUS E-PL10\n- Panasonic GX7MK3(GX9)\n- Canon EOS-RP\n\n## Development\nUse poetry.\n\n```\n# run\n$ poetry run aggexif -h\n\n# build\n$ poetry build aggexif\n\n# local install(after build)\n$ pip install dist/aggexif-x.x.x.tar.gz\n\n# publish\n$ poetry publish\n```\n',
    'author': 'ponkotuy',
    'author_email': 'web@ponkotuy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ponkotuy/python-exif',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
