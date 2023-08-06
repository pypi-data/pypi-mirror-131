# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/dg_util'}

packages = \
['image_preprocessing']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'dlib>=19.22.1,<20.0.0',
 'imutils>=0.5.4,<0.6.0',
 'numpy>=1.21.4,<2.0.0',
 'opencv-python>=4.5.4,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'dg-util',
    'version': '0.0.17',
    'description': 'commom tools',
    'long_description': '# Package dg_util \nv 0.0.15\n\nPackage dg_util consists of different interface of commonly used basic functions in development process to help reduce redoundancy and keep your codes clean. More features will be updated in future.\n* Install: \n\n```bash\npip install dg_util\n```\n\n* Uninstall: \n\n```bash\npip uninstall dg_util\n```\n\n## Features\n### Image Reprocessing\nCrop face images with landmark.\n1. crop_image\n2. crop_image_from_path\n\n### Face Parsing\n\n* Install: \n\n```bash\npip install dg_face_parsing\n```\n\nGenreate face parsing with BiSeNet。\n1. parsing_face\n2. parsing_faces\n\n# Rembg\nRemove background.\n* Requirements\n\npython 3.8 or newer\n\ntorch and torchvision stable version (https://pytorch.org)\n\n* Install:\n\n```bash\npip install rembg\n```\n',
    'author': 'DataGrid',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
