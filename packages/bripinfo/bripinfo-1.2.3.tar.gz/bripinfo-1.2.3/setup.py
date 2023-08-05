# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bripinfo']

package_data = \
{'': ['*'], 'bripinfo': ['.files/.gitkeep']}

install_requires = \
['click>=8.0.0,<9.0.0', 'requests>=2.25.0,<3.0.0', 'urllib3>=1.26.5']

setup_kwargs = {
    'name': 'bripinfo',
    'version': '1.2.3',
    'description': 'Uma maneira fácil de obter dados relativos a um IP associado ao Registro.br.',
    'long_description': '# BrIpInfo\n\n![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/rogeriopaulos/BRIpinfo?label=BRIpinfo&style=flat-square)\n![Python](https://img.shields.io/badge/python-3.8%2B-yellowgreen?style=flat-square)\n![GitHub](https://img.shields.io/github/license/rogeriopaulos/BRIpinfo?style=flat-square)\n\nUma maneira fácil de obter dados relativos a um IP/bloco CIDR associado a um fornecedor de serviço de internet (ISP).\n\nPeriodicamente, o [Registro.br](https://registro.br/) disponibiliza, via [ftp](https://ftp.registro.br/pub/numeracao/origin/nicbr-asn-blk-latest.txt), uma listagem (em um arquivo _.txt_) dos IPs/blocos CIDR ativos no Brasil, bem como a qual fornecedor de serviço de internet o mesmo é associado (juntamente com seu CNPJ).\n\nA partir do desse arquivo, o BrIpInfo analisa e estrutura esses dados de uma forma amigável, permitindo a exportação do mesmo para os formatos _json_ ou _csv_.\n\n## Features\n\n- Obtenção da listagem completa do IPs ativos no Brasil, e suas respectivas ISP\'s, com base no [Registro.br](https://registro.br/);\n- Fácil atualização da listagem disponibilizada;\n- Exportação dos dados em um arquivo _json_ ou _csv_.\n\n## Pré-Requisitos\n\n- [Python 3.8+](https://www.python.org/downloads/)\n- [git](https://git-scm.com/downloads)\n\n## Instalação & Configuração\n\n### Clonar repositório\n\nFaça o clone do repositório da aplicação em um local de sua preferência.\n\n```\ngit clone https://github.com/rogeriopaulos/BRIpinfo.git\n```\n\n### Crie um ambiente virtual [OPCIONAL]\n\nEmbora não seja obrigatório, é recomendável a criação prévia de um ambiente virtual do python. Para maiores informações, veja esse [passo-a-passo](https://cloud.google.com/python/setup?hl=pt-br).\n\n### Instalando as dependências\n\nNo _prompt de comando_ ou _terminal_ do seu sistema operacional, acesse a pasta da aplicação e instale as dependências da mesma executando o comando abaixo.\n\n_Ps: Caso tenha criado um ambiente virtual antes, ative-o._\n\n```\npip install -r requirements.txt\n```\n\n### Setup da aplicação\n\nPara finalizar, execute o _setup_ da aplicação.\n\n**Importante**: Para que o _setup_ da aplicação ocorra normalmente, é necessário uma conexão de internet ativa.\n\n_Ps: Caso tenha criado um ambiente virtual antes, ative-o._\n\n```\npython bripinfo setup\n```\n\n## Comandos & Uso\n\n### Geral\n```\nUsage: bripinfo [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  export  Export data from registro.br to json/csv.\n  query   Query IP or CNPJ from Registro.br.\n  setup   Load data from registro.br.\n```\n\n### Exportação\n\n```\nUsage: bripinfo export [OPTIONS]\n\n  Export data from registro.br to json/csv.\n\nOptions:\n  -f, --format TEXT       Format: [json, csv]. Default: json.\n  -d, --destination TEXT  Where to save. Default: "<current-dir>".\n\n  -n, --name TEXT         Filename. Default: "nicbr-asn-blk-latest"\n  --help                  Show this message and exit.\n```\n\n### Consulta\n\n```\nUsage: bripinfo query [OPTIONS]\n\n  Query IP or CNPJ from Registro.br.\n\nOptions:\n  -t, --type TEXT    Type of query: [ip, cnpj]\n  -s, --search TEXT  Term to searched (ip or cnpj). Ex: 192.168.0.22 (ip) |\n                     10942479000139 (cnpj)\n\n  --help             Show this message and exit.\n```\n\n### Exemplos\n\n```\npython bripinfo export\n```\n...um arquivo no formato _json_ será gerado no diretório corrente onde a aplicação foi baixada (_git clone_).\n\n\n```\npython bripinfo export -f csv -d /home -n "test"\n```\n...um arquivo no formato _csv_, com o nome _"test"_, será gerado no diretório __"/home"__.\n\n```\npython bripinfo query -t ip -s "186.241.20.224"\n\n# output\n{\n    "cnpj": "33.000.118/0001-79",\n    "ips": [\n        "200.223.0.0/16",\n        "200.199.0.0/17",\n        (...)\n    ],\n    "name": "Telemar Norte Leste S.A.",\n    "ref": "AS7738"\n}\n```\n\n\n## Versionamento\n\nEste projeto segue as diretrizes do versionamento semântico (SemVer). Para maiores informações, acesse esse [link](https://semver.org/lang/pt-BR/).\n\n## Licença\n\nVeja o arquivo [LICENÇAS](LICENSE) para saber os direitos e limitações da licença aplicada neste projeto (*MIT*).',
    'author': 'Rogerio Paulo',
    'author_email': 'rogeriopaulos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rogeriopaulos/BRIpinfo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
