# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['face_parsing']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'numpy>=1.21.4,<2.0.0',
 'opencv-python>=4.5.4,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'torch>=1.10.0,<2.0.0',
 'torchaudio>=0.10.0,<0.11.0',
 'torchvision>=0.11.1,<0.12.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'dg-face-parsing',
    'version': '0.0.4',
    'description': 'Face parsing tools with BiSeNet',
    'long_description': '\n### Face Parsing\nGenreate face parsing with BiSeNet。\npip install dg_face_parsing\n1. parsing_face\n2. parsing_faces\n\n### Usage\n1. dg_util.face_parsing.parsing_face(input_path, output_path)\n*input_img- Image data()PIL.image.\n*output_path- File path of output image(string, Blank as default).Opional, if output_path is blank, result image returned as cv2.image. Else, result image saved in output path and True returned.\n*Return- Image data || Nones\n2. dg_util.face_parsing.parsing_faces(input_folder, output_folder)\n*Return- None\n*input_folder- File path of input folder(string).\n*output_folder- File path of output folder(string).',
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
