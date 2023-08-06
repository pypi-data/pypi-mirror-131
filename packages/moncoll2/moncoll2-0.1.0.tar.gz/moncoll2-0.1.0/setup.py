# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['moncoll2']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'moncoll2',
    'version': '0.1.0',
    'description': '',
    'long_description': 'pymongoの単純なラッパー。接続情報、db_name、collection_nameをまとめてdictに含めることでDB操作のコードをシンプルにする。\n\n[comment]: <> ([![Test]&#40;https://github.com/atu4403/moncoll2/actions/workflows/test.yml/badge.svg&#41;]&#40;https://github.com/atu4403/moncoll2/actions/workflows/test.yml&#41;)\n\n[comment]: <> ([![PyPI version]&#40;https://badge.fury.io/py/moncoll2.svg&#41;]&#40;https://badge.fury.io/py/moncoll2&#41;)\n\n[comment]: <> (document link)\n\n[comment]: <> (## Install)\n\n[comment]: <> (```bash)\n\n[comment]: <> (pip install moncoll2)\n\n[comment]: <> (```)\n\n## Useit\n\n### MC(settings: dict)-> pymongo.collection.Collection\n\nsettingsを元にしてcollectionを返す。with構文の中で操作をする事によってDBのcloseを確実に行う。\n\n```py\nfrom moncoll2 import MC\n\nsettings = {\n    "username": "testuser",\n    "password": "testpass",\n    "host": "192.168.0.99",\n    "port": 12345,\n    "coll_name": "test_collenction",\n    "db_name": "test_db"\n}\n\nwith MC(settings) as coll:\n    assert coll.full_name == \'test_db.test_collenction\'\n    coll.insert_one({"a": 1})\n    res = coll.find_one()\n    assert res[\'a\'] == 1\n    coll.drop()\n```\n\n#### Args\n\nsettings (dict): pymongoのMongoClientに渡す引数にdb_nameとcollection_nameを加えたもの\n\n[mongo_client – Tools for connecting to MongoDB — PyMongo 4.0.1 documentation](https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html)\n\n### to_bulklist(_list: list, idname: str = "_id") -> list:\n\nlistをbulk_writeで使用できる形式にする\n\n#### Args\n\n_list (list): 元になるlist idname (str): _idになる項目名、元になるlistに含まれるなら省略可能\n\n#### Returns\n\nlist: bulk_writeで使用できる形式のlist\n\n#### Raises\n\nBulkItemNotIdError: 元のlistに`_id`という項目が含まれておらず、かつ引数`idname`が指定されていない場合に発生\n\n#### Examples:\n\n```python\n>>> li = [\n...     {"name": "Karin", "gender": "female"},\n...     {"name": "Decker", "gender": "male"}\n... ]\n>>> res = to_bulklist(li, \'name\')\n>>> res[0]\nUpdateOne({\'_id\': \'Karin\'}, {\'$set\': {\'name\': \'Karin\', \'gender\': \'female\', \'_id\': \'Karin\'}}, True, None, None, None)\n```\n',
    'author': 'atu4403 ',
    'author_email': '73111778+atu4403@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atu4403',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
