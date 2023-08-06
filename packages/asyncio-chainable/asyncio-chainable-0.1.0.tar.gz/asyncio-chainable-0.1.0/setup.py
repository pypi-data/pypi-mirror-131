# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_chainable']

package_data = \
{'': ['*']}

install_requires = \
['pytest-asyncio>=0.16.0,<0.17.0',
 'pytest[test]>=6.2.4,<7.0.0',
 'setuptools>=57.4.0,<58.0.0']

setup_kwargs = {
    'name': 'asyncio-chainable',
    'version': '0.1.0',
    'description': 'Making asyncio coroutines chainable',
    'long_description': '# asyncio-chainable\n\nMaking asyncio coroutines chainable\n\nBuilt on: Python3 and Docker (alpine) and Poetry (Package Manager)<br>\nMaintained by: Chris Lee [sihrc.c.lee@gmail.com]\n\n## Example Usage\n```python3\nimport pytest\n\nfrom asyncio_chainable import async_chainable, async_chainable_class\n\n\n@pytest.mark.asyncio\nasync def test_simple_chain():\n    class Number:\n        def __init__(self, num: int = 0):\n            self.num = num\n\n        @async_chainable\n        async def add(self, num: int):\n            self.num += num\n            return self\n\n        @async_chainable\n        async def subtract(self, num: int):\n            self.num -= num\n            return self\n\n    assert (await Number().add(5).subtract(2)).num == 3\n\n\n@pytest.mark.asyncio\nasync def test_class_chain():\n    @async_chainable_class\n    class Number:\n        def __init__(self, num: int = 0):\n            self.num = num\n\n        async def add(self, num: int):\n            self.num += num\n            return self\n\n        async def subtract(self, num: int):\n            self.num -= num\n            return self\n\n    assert (await Number().add(5).subtract(2)).num == 3\n```\n\n## Contributing: Getting Started\n\n### Docker\n\n- Additional Python3 dependencies can be added to requirements.txt<br>\n- Tests are located in ./tests <br>\n- To run the docker container with the basic requirements, dependencies, and the package installed:\n  ```bash\n  $ touch .env\n  $ docker-compose up\n  ```\n\n### Poetry\n\n```\n$ poetry install\n```\n',
    'author': 'Chris Lee',
    'author_email': 'sihrc.c.lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sihrc/asyncio-chainable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
