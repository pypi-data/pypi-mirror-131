# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_contextmanager_pool']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.8" and python_version < "3.9"': ['typing-extensions>=3.10.0.0']}

setup_kwargs = {
    'name': 'asyncio-contextmanager-pool',
    'version': '0.1.2',
    'description': 'A library providing a pool-like object for holding `AsyncContextManager` instances.',
    'long_description': '# asyncio-contextmanager-pool\n\nA library providing a pool-like object for holding `AsyncContextManager` instances.\n\n## Why?\n\nSome objects, like MongoDB connections to a Replica Set, are expensive to create, time-wise. As a result, they are usually created once and then used across the entire application. This mitigates, or eliminates, the costs associated with creating and setting up such objects.\n\nHowever, there are situations where one may need to dynamically create such objects. One such example would be a multi-tenant API that can talk to multiple instances.\n\nOne could use `cachetools` to hold the references, perhaps in a `TTLCache`, so that not "too many" instances are kept (especially when not used), but then they must also make sure that instances are cleaned up properly, sometimes with some leniency (TTL).\n\n## Features\n\n- Async Context Manager (`async with`) support to manage objects\n- Memoizes instances based on the arguments used to create them, which prevents duplicates and saves init time\n- Provides TTL support, so that objects are kept for a set period of time after not being used, which again helps preventing duplication\n\n## Usage\n\n```python\nimport asyncio\nfrom asyncio_contextmanager_pool import Pool\n\n\nclass Example:\n    """\n    A dummy implementation of an AsyncContextManager\n    that "knows" when it was used.\n    """\n    def __init__(self, message: str) -> None:\n        self.message = message\n\n        self.enter_called = 0\n        self.exit_called = 0\n\n    async def __aenter__(self):\n        self.enter_called += 1\n        return self\n\n    async def __aexit__(self, *args, **kwargs):\n        self.exit_called += 1\n\n\nasync with Pool(Example, ttl=5) as p:\n    # Get an instance of Example\n    async with p.get("hello, world") as inst_1:\n        # Use it\n        assert inst_1.message == "hello, world"\n\n    # Here, under normal circumstances, `inst_1` is still alive\n    assert inst_1.exit_called == 0\n\n    # So, if I `get` it again...\n    async with p.get("hello, world") as inst_2:\n        # And use it...\n        assert inst_2.message == "hello, world"\n    \n    # I will get the exact same object\n    assert inst_1 is inst_2\n\n    # Now, let\'s assume some time passes...\n    await asyncio.sleep(10)\n\n    # Here, inst_1 already expired, so inst_3\n    # will be a new object...\n    async with p.get("hello, world") as inst_3:\n        assert inst_3.message == "hello, world"\n\n    assert inst_1 is not inst_3\n    assert inst_1.exit_called == 1\n\n# And after the `async with` block, everything is cleaned:\nassert inst_3.exit_called == 1\n```\n\n## Notes\n\n### Pickle support\n\nIf a `Pool` instance is copied via Pickle (e.g., through `multiprocessing.Process` or a `concurrent.futures.ProcessPoolExecutor`), the instances are not copied.\n\nThis is by design, because:\n\n- Some objects should not be copied between processes (e.g., `pymongo.MongoClient`)\n- Object expiration uses `asyncio`\'s Timer functions, which are attached to the Event Loop. Event Loops cannot be shared between processes.\n',
    'author': 'André Carvalho',
    'author_email': 'afecarvalho@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RedRoserade/asyncio-contextmanager-pool',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
