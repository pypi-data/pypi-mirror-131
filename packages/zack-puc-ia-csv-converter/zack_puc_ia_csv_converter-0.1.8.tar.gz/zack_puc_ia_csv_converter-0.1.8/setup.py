# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zack_puc_ia_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.5,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'zack_puc_ia_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'zack-puc-ia-csv-converter',
    'version': '0.1.8',
    'description': 'Convert CSV to JSON or JSON to CSV',
    'long_description': '# Arquivo Converter\n\n- **CSV** para conversor **JSON**.\n- **JSON** para conversor **CSV**.\n\n## Introdução\n\n### O que este projeto pode fazer\n\n- Leia um arquivo **CSV** ou uma pasta com **CSV** e converta-os em **JSON**.\n- Leia um arquivo **JSON** ou uma pasta com **JSON** e converta-os em **CSV**.\n\nEste projeto é um programa em execução no terminal, de preferência instalado com pipx:\n\n`` `\npipx install zack-puc-ia-csv-converter\n`` `\n\nPara usar, basta digitar:\n\n`` `\n$ converter --help\n`` `\n\n### Isso listará todas as opções disponíveis.\n  Converta um único arquivo ou lista de arquivos **CSV** para **JSON** ou arquivos **JSON** para arquivos **CSV**.\n\nOpcoes:\n-  -t, --type TEXT             Tipo de arquivo que será lido é convertido(CSV ou JSON).\n-  -i, --input TEXT            Caminho onde os arquivos serão carregados para conversão.\n-  -o, --output TEXT           Caminho onde os arquivos convertidos serão salvos.\n-  -d, --delimiter [,|;|:|\\t]  Separador usado para dividir os arquivos.\n-  -p, --prefix TEXT           Prefixo de TEXTO usado para preceder ao nome do convertido\n                               arquivo salvo no disco. O sufixo será um número\n                               começando de 1 a N.Caso nao seja passado nenhum prefixo será utilizado o file_.\n-  --help                      Mostra esta mensagem e sai.\n',
    'author': 'ezequiel lima ',
    'author_email': 'ezekiel_lima@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
