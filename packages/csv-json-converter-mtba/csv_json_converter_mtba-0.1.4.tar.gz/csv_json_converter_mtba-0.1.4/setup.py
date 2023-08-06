# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_json_converter_mtba']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_json_converter = '
                     'csv_json_converter_mtba.converter:converter']}

setup_kwargs = {
    'name': 'csv-json-converter-mtba',
    'version': '0.1.4',
    'description': 'Conversor CSV-JSON',
    'long_description': '# CSV-JSON Converter\n\nConversor de CSV para JSON / JSON para CSV.\n\n## Introduction\n\nTrabalho desenvolvido para a disciplina Python para Ciência de Dados do curso de pós-graduação em Ciência de Dados e Big Data da PUC Minas - 2021.\n\n### What this project can do\n\nLê arquivos **csv/json** e os converte para **csv/json**.\nEste projeto é um programa de execução no terminal.\nInstalar preferencialmente com pipx:\n\n```bash\npipx install csv_json_converter_mtba\n```\n\nPara usar, digite:\n\n```bash\ncsv_json_converter --help\n```\n\nEsse comando listará todas as opções disponíveis.',
    'author': 'Marco Andrade',
    'author_email': 'marcotbandrade@gmail.com',
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
