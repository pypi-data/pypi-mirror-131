# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fellipems_csv_json_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pandas>=1.3.3,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'fellipems_csv_json_converter.converter:Converte_JSONCSV']}

setup_kwargs = {
    'name': 'fellipems-csv-json-converter',
    'version': '0.1.7',
    'description': 'Curso de introducao ao python: Conversor CSV-JSON',
    'long_description': "# File Converter\n\nCSV / JSON converter\n\n### project\n\nfuncao: Converte_JSONCSV(modo,sep)\n\nConverte um arquivo ou pasta de arquivos do formato **CSV** para **JSON**. a funcao possui as variaveis 'modo' (opcional), \n'sep' (opcional) e 'Arq' (obrigatorio)\n        \n       Arq: um arquivo ou pasta (string). caso seja passado para a funcao um unico arquivo, este sera convertido. \n       Caso seja passada uma pasta, serao convertidos todos os arquivos do tipo compativel\n       \n           Obs.:os arquivos convertidos serao salvos na mesma pasta do arquivo original e com mesmo nome, sobrescrevendo \n           arquivos que eventualmente existam na pasta\n       \n       modo: o modo padrao de conversao e CSV para JSON (modo='csv2json'), porem caso seja passado o parametro 'json2csv' \n       na variavel 'modo', a conversao sera feita no sentido contrario\n       \n       sep : o separador padrao para o arquivo CSV sera ',' (virgula), porem um separador diferente pode ser especificado \n       atraves da variavel 'sep'\n\npip install fellipems_csv_json_converter\n\n#csv_converter --help\n",
    'author': 'FellipeMS',
    'author_email': 'fellipems.sc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
