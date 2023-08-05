# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['artur_tancredo_alvarenga_puc_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'artur_tancredo_alvarenga_puc_csv_converter.converter:converter',
                     'json_converter = '
                     'artur_tancredo_alvarenga_puc_csv_converter.converter:converter_2']}

setup_kwargs = {
    'name': 'artur-tancredo-alvarenga-puc-csv-converter',
    'version': '0.1.11',
    'description': 'Trabalho da PUC - converter arquivo(s) de csv para json e json para csv',
    'long_description': '# Conversão de arquivos:\n\n.CSV para JSON\n.JSON para CSV.\n\n## Introdução\n\nEsse é um trabalho proposta na disciplina de Python da Pós Graduação da PUC-MG, cujo objetivo é usar o PATH para a conversão de arquivos de CSV para JSON e/ou JSON para CSV.\n\n### O que o projeto faz ?\n\nLer um arquivo de **CSV** ou **JSON** e até mesmo, ler uma pasta com arquivos de **CSV** ou **JSON** , cujo objetivo é converter **CSV-JSON** ou **JSON-CSV**. Este projeto é um programa de execução no terminal, de preferÊncia instalado com **pipx**:\n\n```bash\npipx install artur_tancredo_alvarenga_puc_csv_converter\n```\n\nPara usar, basta digitar:\n\n### Converter CSV para JSON\n\n```bash\ncsv_converter --help\n```\n\n### Converter JSON para CSV\n\n```bash\njson_converter --help\n```\n\n### Isso listará todas as opções disponíveis.',
    'author': 'Artur Tancredo de Alvarenga',
    'author_email': 'arturalvarenga@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
