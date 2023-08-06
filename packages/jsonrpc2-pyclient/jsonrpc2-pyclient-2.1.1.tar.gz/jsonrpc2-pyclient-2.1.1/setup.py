# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonrpc2pyclient']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.1,<0.22.0', 'jsonrpc2-objects>=1.3.7,<2.0.0']

setup_kwargs = {
    'name': 'jsonrpc2-pyclient',
    'version': '2.1.1',
    'description': 'Python JSON-RPC 2.0 client library.',
    'long_description': '<div align="center">\n<!-- Title: -->\n  <h1>JSON RPC PyClient</h1>\n<!-- Labels: -->\n  <!-- First row: -->\n  <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg"\n   height="20"\n   alt="License: AGPL v3">\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"\n   height="20"\n   alt="Code style: black">\n  <img src="https://img.shields.io/pypi/v/jsonrpc2-pyclient.svg"\n   height="20"\n   alt="PyPI version">\n  <a href="https://gitlab.com/mburkard/jsonrpc-pyclient/-/blob/main/CONTRIBUTING.md">\n    <img src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=00b250"\n     height="20"\n     alt="Contributions Welcome">\n  </a>\n  <h3>A library for creating JSON RPC 2.0 clients in Python with async support</h3>\n</div>\n\n## Install\n\n```shell\npip install jsonrpc2-pyclient\n```\n\n## Usage\n\n### RPC Client Abstract Class\n\nThe RPCClient abstract class provides methods to ease the development of\nan RPC Client for any transport method. It parses JSON-RPC 2.0 requests\nand responses.\n\nTo use, an implementation only needs to override the\n`_send_and_get_json` method. This method is used internally.\nJSONRPCClient will pass it a request as a JSON string and expect a\nresponse as JSON string.\n\nA simple implementation:\n\n```python\nclass RPCHTTPClient(RPCClient):\n\n    def __init__(self, url: str) -> None:\n        self.url = url\n        super(RPCHTTPClient, self).__init__()\n\n    def _send_and_get_json(self, request_json: str) -> Union[bytes, str]:\n        return requests.post(url=self.url, data=request_json).content\n```\n\n### Default HTTP Client\n\nThis module provides a default HTTP implementation of the RPCClient.\n\n#### Example HTTP Client Usage\n\nIf a JSON RPC server defines the methods "add", "subtract", and\n"divide", expecting the following requests:\n\n```json\n{\n  "id": 1,\n  "method": "add",\n  "params": [2, 3],\n  "jsonrpc": "2.0"\n}\n\n{\n  "id": 2,\n  "method": "subtract",\n  "params": [2, 3],\n  "jsonrpc": "2.0"\n}\n\n{\n  "id": 3,\n  "method": "divide",\n  "params": [3, 2],\n  "jsonrpc": "2.0"\n}\n```\n\nDefining and using the corresponding client would look like this:\n\n```python\nclass MathClient(RPCHTTPClient):\n    def add(self, a: int, b: int) -> int:\n        return self.call(\'add\', [a, b])\n\n    def subtract(self, a: int, b: int) -> int:\n        return self.call(\'subtract\', [a, b])\n\n    def divide(self, a: int, b: int) -> float:\n        return self.call(\'divide\', [a, b])\n\n\nclient = MathClient(\'http://localhost:5000/api/v1\')\nclient.add(2, 3)  # 5\nclient.subtract(2, 3)  # -1\nclient.divide(2, 2)  # 1\n```\n\nNotice, just the result field of the JSON-RPC response object is\nreturned by `call`, not the whole object.\n\n## Errors\n\nIf the server responds with an error, an RpcError is thrown.\n\nThere is an RpcError for each standard JSON RPC 2.0 error, each of them\nextends RpcError.\n\n```python\nclient = MathClient(\'http://localhost:5000/api/v1\')\n\ntry:\n    client.add(\'two\', \'three\')\nexcept InvalidParams as e:\n    log.exception(f\'{type(e).__name__}:\')\n\ntry:\n    client.divide(0, 0)\nexcept ServerError as e:\n    log.exception(f\'{type(e).__name__}:\')\n```\n\n### Async Support (v1.1+)\n\nAsync alternatives to the RPCClient ABC and RPCHTTPClient are available.\n\n```python\nclass AsyncMathClient(AsyncRPCHTTPClient):\n    async def add(self, a: int, b: int) -> int:\n        return await self.call(\'add\', [a, b])\n\n    async def subtract(self, a: int, b: int) -> int:\n        return await self.call(\'subtract\', [a, b])\n\n    async def divide(self, a: int, b: int) -> float:\n        return await self.call(\'divide\', [a, b])\n```\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/jsonrpc2-pyclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
