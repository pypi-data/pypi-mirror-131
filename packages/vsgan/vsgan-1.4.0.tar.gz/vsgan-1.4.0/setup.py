# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vsgan']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0']

setup_kwargs = {
    'name': 'vsgan',
    'version': '1.4.0',
    'description': 'VapourSynth Single Image Super-Resolution Generative Adversarial Network (GAN)',
    'long_description': '![banner](https://rawcdn.githack.com/rlaphoenix/VSGAN/d7ad537bffb52bdbd1ad07c825cf016964ac57a2/banner.png)\n\n[![Build Tests](https://img.shields.io/github/workflow/status/rlaphoenix/VSGAN/Version%20test?label=Python%203.6%2B%20builds)](https://github.com/rlaphoenix/VSGAN/actions?query=workflow%3A%22Version+test%22)\n[![License](https://img.shields.io/github/license/rlaphoenix/VSGAN?style=flat)](https://github.com/rlaphoenix/VSGAN/blob/master/LICENSE)\n[![DeepSource](https://deepsource.io/gh/rlaphoenix/VSGAN.svg/?label=active+issues)](https://deepsource.io/gh/rlaphoenix/VSGAN/?ref=repository-badge)\n<a href="https://colab.research.google.com/github/rlaphoenix/VSGAN/blob/master/VSGAN.ipynb">\n    <img align="right" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/>\n</a>\n\nVSGAN is a Single Image Super-Resolution Generative Adversarial Network (GAN) which uses the VapourSynth processing framework to handle input and output image data.\n\n## Documentation\n\nMore information, installation, building, quick start, and more, is available at [rlaphoenix.github.io/VSGAN](https://rlaphoenix.github.io/VSGAN).\n\nThe source code to the Documentation page is available on the [gh-pages branch](https://github.com/rlaphoenix/VSGAN/tree/gh-pages) and can be built and deployed locally.  \nYou could also just read the markdown files found in the [_docs folder](https://github.com/rlaphoenix/VSGAN/tree/gh-pages/_docs).\n\n## License\n\nThis project is released under the MIT license.  \nPlease read and agree to the license before use, it can be found in the [LICENSE](LICENSE) file.\n',
    'author': 'PHOENiX',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlaphoenix/vsgan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
