# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['findsub', 'findsub.core']

package_data = \
{'': ['*'], 'findsub': ['data/*', 'scripts/*']}

install_requires = \
['Cython>=0.29.26,<0.30.0',
 'IMDbPY>=2021.4.18,<2022.0.0',
 'aiofiles>=0.8.0,<0.9.0',
 'aiohttp[speedups]>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'lxml>=4.7.1,<5.0.0',
 'setuptools>=59.6.0,<60.0.0',
 'srt>=3.5.0,<4.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'webrtcvad>=2.0.10,<3.0.0',
 'wheel>=0.37.0,<0.38.0']

entry_points = \
{'console_scripts': ['findsub = findsub.__main__:run']}

setup_kwargs = {
    'name': 'findsub',
    'version': '0.0.5',
    'description': 'Finding and ranking subtitles from subscene by how much they are synced.',
    'long_description': '# FindSub\n\nFindSub is an Application for automatically downloading and ranking subtitles based on how much they are synced\nfrom [subscene](https://subscene.com/).\n**Compatible With Unix Systems.**\n\n\n## Installation\n\nRecommended way is by using [pipx](https://github.com/pypa/pipx).\nFirst, install pipx:\n\n```bash\nsudo apt install pipx\n```\n\nThen install FindSub by using the command below:\n\n```bash\npipx install --python python3.9 findsub\n```\n\nP.S.: FindSub is supported by python3.9+. Also, GCC is required for compiling C extensions.\nFFmpeg and FFprobe are also needed for extracting of movie\'s audio.\n\n# Basic Usage and explanation. (Must read!)\n\n```bash\nfindsub The.French.Dispatch.2021.1080p.WEB-DL.x264.6CH-Pahe.FilmBan.mkv\n```\n→ First, findsub try to guess the name of the movie based on the filename and with the help of IMDB. \nSimultaneously it will extract the movie\'s audio by using "**FFmpeg**"  and "**FFprobe**". \nIf a cached extracted audio is present in the same directory, findsub will skip this stage and use it instead.\nAt the same time, findsub tries to download the subtitles from subscene in the desired language.\nYou can use -l/--language to select a language (ISO 639-1). if nothing is specified with this option, \n**findsub will try to use "FINDSUB_LANG" environment variable** and if nothing is set, it will use "En" as default.\nSometimes, especially when the original movie name is not in English, findsub cannot find the paired subscene page, \nand you should manually set the subscene link of the page with the help of -s/--subscene option.\n\n\n# Advance Usage\n## Languages \n\n```bash\nfindsub The.French.Dispatch.2021.1080p.WEB-DL.x264.6CH-Pahe.FilmBan.mkv --language "fa";\n```\nOR\n```\nexport FINDSUB_LANG="fa"; findsub The.French.Dispatch.2021.1080p.WEB-DL.x264.6CH-Pahe.FilmBan.mkv\n```\n→ With these two approaches, you can set the language.\nYou must use two-letter codes based on (ISO 639-1). \nP.S.: **exceptionally, use "bz" for Brazillian Portuguese.**\n\n## Speeding up\n```bash\nfindsub The.French.Dispatch.2021.1080p.WEB-DL.x264.6CH-Pahe.FilmBan.mkv --audio ./already_extraced_audio.wav\n```\nOR\n```bash\nfindsub The.French.Dispatch.2021.1080p.WEB-DL.x264.6CH-Pahe.FilmBan.mkv --synced-subtitle ./synced_sub.srt\n```\n→ use an already extracted audio or a sync subtitle to speed up the program.\n```bash\nfindsub The.French.Dispatch.2021.1080p.WEB-DL.x264.6CH-Pahe.FilmBan.mkv --subtitles-directory downloaded_sub/\n```\n→ Skip downloading subtitles and rank the subtitles within the mentioned directory.\n\n## -s/--subscene\n```bash\nsubfinder The_Sea_Inside_2004_720p_BrRip_YIFY.mkv -s https://subscene.com/subtitles/the-sea-inside-mar-adentro\n```\n→ Sometimes FindSub cannot find the subscene page for a movie, in that case, you should manually pass the link to it.\n- check `findsub --help` for more info.\n\n## Dependencies\n**FFmpeg, FFprobe, Bash, and Iconv** are needed in most cases.\n\n\n## Issues\nFindsub currently doesn\'t support downloading subtitles for series episodes. \nAlso, it may not work very well with windows, but it should be usable.\n\n\n## Contributing\n    Written by: Mahyar Mahdavi <Mahyar@Mahyar24.com>.\n    License: GNU GPLv3.\n    Source Code: <https://github.com/mahyar24/FindSub>.\n    PyPI: <https://pypi.org/project/FindSub/>.\n    Reporting Bugs and P.R.s are welcomed. :)\n\n## License\n[GPLv3](https://choosealicense.com/licenses/gpl-3.0)\n',
    'author': 'Mahyar Mahdavi',
    'author_email': 'Mahyar@Mahyar24.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mahyar24/FindSub/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
