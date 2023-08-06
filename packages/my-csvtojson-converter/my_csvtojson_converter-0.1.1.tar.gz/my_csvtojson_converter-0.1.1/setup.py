# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_csvtojson_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'my_csvtojson_converter.converter:converter']}

setup_kwargs = {
    'name': 'my-csvtojson-converter',
    'version': '0.1.1',
    'description': 'Converte arquivos .csv para .json. Publicado apenas para fins educativos da PUC/Minas, classe de Pós Graduação.',
    'long_description': "# My_CSVtoJSON_Converter\n\nmy_csvtojson_converter é um simples conversor de arquivos .csv para o formato .json e vice-versa.\n\nAs funções recebem, basicamente: um input contendo um Path (caminho do arquivo) e um delimitador em formato string (, ou ;).\n\n\n## Função leitura de .csv\n\n*'leitor_csv(input_path: Path, delimiter: str = ',' or ';')'\n\n",
    'author': 'Mirian Machado',
    'author_email': 'miriancosta.m@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
