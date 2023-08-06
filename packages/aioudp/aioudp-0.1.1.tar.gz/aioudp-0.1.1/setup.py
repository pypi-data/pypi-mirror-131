# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioudp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aioudp',
    'version': '0.1.1',
    'description': 'A better API for asynchronous UDP',
    'long_description': '# AioUDP\n\n[![Documentation Status](https://readthedocs.org/projects/aioudp/badge/?version=latest)](https://aioudp.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/ThatXliner/aioudp/branch/main/graph/badge.svg?token=xZ7HVG8Owm)](https://codecov.io/gh/ThatXliner/aioudp) [![CI](https://github.com/ThatXliner/aioudp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ThatXliner/aioudp/actions/workflows/ci.yml)\n\n> A better API for asynchronous UDP\n\nA [websockets](https://websockets.readthedocs.io/en/stable/index.html)-like API for [UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)\n\nHere\'s an example echo server:\n\n```py\nimport asyncio\nimport signal\n\nimport aioudp\n\n\nasync def main():\n    async def handler(connection):\n        async for message in connection:\n            await connection.send(message)\n\n    # Optional. This is for properly exiting the server when Ctrl-C is pressed\n    # or when the process is killed/terminated\n    loop = asyncio.get_running_loop()\n    stop = loop.create_future()\n    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)\n    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)\n\n    # Serve the server\n    async with aioudp.serve("localhost", 9999, handler):\n        await stop  # Serve forever\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\nAnd a client to connect to the server:\n\n```py\nimport asyncio\n\nimport aioudp\n\n\nasync def main():\n    async with aioudp.connect("localhost", 9999) as connection:\n        await connection.send(b"Hello world!")\n        assert await connection.recv() == b"Hello world!"\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\nNOTE: This library provides no other abstractions over the existing UDP interface in `asyncio` other than the `async`/`await`-based API. This means there is no implicit protocol handled in this library. You must write your own.\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/aioudp',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
