# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['listdiff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'listdiff',
    'version': '1.0.0',
    'description': 'Diff 2 python lists using a given key',
    'long_description': '# Overview\n\nDiff 2 python lists using a given key\n\n[![image](https://codecov.io/gh/rkhwaja/pylistdiff/branch/master/graph/badge.svg)](https://codecov.io/gh/rkhwaja/pylistdiff)\n\n# Usage\n\n``` python\nlistA = [3, 2, 1]\nlistB = [5, 4, 3]\ninA, inBoth, inB = DiffUnsortedLists(listA=listA, listB=listB, keyA=lambda x: x, keyB=lambda x: x)\nassert inA == [1, 2]\nassert inBoth == [(3, 3)]\nassert inB == [4, 5]\n\nlistA = [1, 2, 3]\nlistB = [3, 4, 5]\nresultB = DiffListsByKey(iterA=iter(listA), iterB=iter(listB), keyA=lambda x: x, keyB=lambda x: x)\nassert inA == [1, 2]\nassert inBoth == [(3, 3)]\nassert inB == [4, 5]\n```\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/pylistdiff',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
