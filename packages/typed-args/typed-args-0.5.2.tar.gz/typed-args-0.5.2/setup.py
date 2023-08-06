# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_args']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'typed-args',
    'version': '0.5.2',
    'description': 'Parse command line arguments by defining dataclasses',
    'long_description': '# TypedArgs\n\n[![Build Status](https://travis-ci.org/SunDoge/typed-args.svg?branch=master)](https://travis-ci.org/SunDoge/typed-args)\n[![Version](https://img.shields.io/pypi/v/typed-args)](https://pypi.org/project/typed-args/)\n\nStrong type args.\n\nThis project is inspired by [TeXitoi/structopt](https://github.com/TeXitoi/structopt).\n\n## Install\n\nFrom pypi\n\n```bash\npip install typed-args\n```\n\nIf you want to use it on python 3.5 and 3.6 please install `dataclasses`:\n\n```bash\npip install dataclasses\n```\n\n## Usage\n\n\n```python\nimport argparse\nfrom dataclasses import dataclass\n\nimport typed_args as ta\n\n"""\nargparse\n"""\nparser = argparse.ArgumentParser()\nparser.add_argument(\n    \'data\', metavar=\'DIR\', type=str,\n    help=\'path to dataset\'\n)\nparser.add_argument(\n    \'-a\', \'--arch\', metavar=\'ARCH\', default=\'resnet18\', type=str,\n    help=\'model architecture (default: resnet18)\'\n)\nparser.add_argument(\n    \'-j\', \'--workers\', default=4, metavar=\'N\', type=int, dest=\'num_workers\',\n    help=\'number of data loading workers (default: 4)\'\n)\n\n"""\nTypedArgs\n"""\n\n\n@dataclass\nclass Args(ta.TypedArgs):\n    data: str = ta.add_argument(\n        metavar=\'DIR\', type=str, help=\'path to dataset\'\n    )\n    arch: str = ta.add_argument(\n        \'-a\', \'--arch\', metavar=\'ARCH\', default=\'resnet18\', type=str,\n        help=\'model architecture (default: resnet18)\'\n    )\n    num_workers: int = ta.add_argument(\n        \'-j\', \'--workers\', default=4, metavar=\'N\', type=int,\n        help=\'number of data loading workers (default: 4)\'\n    )\n\n\ndef test_args():\n    data = \'/path/to/dataset\'\n    arch = \'resnet50\'\n    num_workers = 8\n\n    argv = f\'{data} -a {arch} --workers {num_workers}\'.split()\n\n    """\n    from_args = parse_args, from_known_args = parse_known_args\n    """\n    typed_args = Args.from_args(argv)\n    args = parser.parse_args(argv)\n\n    assert args.arch == typed_args.arch\n    assert args.data == typed_args.data\n    assert args.num_workers == typed_args.num_workers\n\n\nif __name__ == "__main__":\n    test_args()\n```\n\n## Limitation\n\nCurrently, we don\'t support `add_group` and `sub parser`, but we will.',
    'author': 'SunDoge',
    'author_email': '384813529@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
