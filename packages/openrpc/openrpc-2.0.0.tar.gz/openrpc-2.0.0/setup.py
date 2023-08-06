# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrpc']

package_data = \
{'': ['*']}

install_requires = \
['jsonrpc2-objects>=1.3.7,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'openrpc',
    'version': '2.0.0',
    'description': 'OpenRPC provides classes to rapidly develop an OpenRPC server.',
    'long_description': '<div align=center>\n  <h1>OpenRPC</h1>\n  <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg"\n   height="20"\n   alt="License: AGPL v3">\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"\n   height="20"\n   alt="Code style: black">\n  <img src="https://img.shields.io/pypi/v/openrpc.svg"\n   height="20"\n   alt="PyPI version">\n  <a href="https://gitlab.com/mburkard/openrpc/-/blob/main/CONTRIBUTING.md">\n    <img src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=2267a0"\n     height="20"\n     alt="Contributions Welcome">\n  </a>\n  <h3>OpenRPC provides classes to rapidly develop an\n  <a href="https://open-rpc.org">OpenRPC</a> server.</h3>\n</div>\n\n## Installation\n\nOpenRPC is on PyPI and can be installed with:\n\n```shell\npip install openrpc\n```\n\n## Usage\n\nThis library provides an `OpenRPCServer` class that can be used to\nquickly create an OpenRPCServer; it takes as an argument an `InfoObject`\nwhich needs at minimum a title and version.\n\n```python\nfrom openrpc.objects import InfoObject\nfrom openrpc.server import OpenRPCServer\n\nrpc = OpenRPCServer(InfoObject(title="Demo Server", version="1.0.0"))\n```\n\n### Register a function as an RPC Method\n\nTo register a method with the OpenRPCServer add the `@rpc.method`\ndecorator to a method.\n\n```python\n@rpc.method\ndef add(a: int, b: int) -> int:\n    return a + b\n```\n\n#### RPC Discover\n\nThe `rpc.discover` method is automatically generated. It relies heavily\non type hints.\n\n### Process JSON RPC Request\n\nOpenRPC is transport agnostic. To use it, pass JSON RPC requests to the\n`process_request` method.\n\n```python\nreq = """\n{\n  "id": 1,\n  "method": "add",\n  "params": {"a": 2, "b": 2},\n  "jsonrpc": "2.0"\n}\n"""\nrpc.process_request(req)  # \'{"id": 1, "result": 4, "jsonrpc": "2.0}\'\n```\n\n### Async Support (v1.2+)\n\nOpenRPC has async support:\n\n```python\nawait rpc.process_request_async(req)\n```\n\n### Pydantic Support\n\nFor data classes, it is strongly recommended you use Pydantic.\nOpenRPCServer will use Pydantic for JSON serialization/deserialization\nas well as generating schemas.\n\n## Example\n\n```python\nfrom flask import Flask, Response, request\nfrom openrpc.objects import InfoObject\nfrom openrpc.server import OpenRPCServer\nfrom pydantic import BaseModel\n\napp = Flask(__name__)\nrpc = OpenRPCServer(InfoObject(title="Demo Server", version="1.0.0"))\n\n\nclass Vector3(BaseModel):\n    x: float\n    y: float\n    z: float\n\n\n@rpc.method\ndef get_distance(a: Vector3, b: Vector3) -> Vector3:\n    return Vector3(\n        x=a.x - b.x,\n        y=a.y - b.y,\n        z=a.z - b.z,\n    )\n\n\n@rpc.method\ndef add(a: int, b: int) -> int:\n    return a + b\n\n\n@app.route("/api/v1/", methods=["POST"])\ndef process_rpc() -> str:\n    return rpc.process_request(request.data)\n\n\nif __name__ == "__main__":\n    app.run()\n```\n\nExample In\n\n```json\n[\n  {\n    "id": 1,\n    "method": "add",\n    "params": {"a": 1, "b": 3},\n    "jsonrpc": "2.0"\n  }, {\n    "id": 2,\n    "method": "add",\n    "params": [5, 7],\n    "jsonrpc": "2.0"\n  }, {\n    "id": 3,\n    "method": "add",\n    "params": [11, "thirteen"],\n    "jsonrpc": "2.0"\n  }\n]\n```\n\nExample Result Out\n\n```json\n[\n  {\n    "id": 1,\n    "result": 4,\n    "jsonrpc": "2.0"\n  }, {\n    "id": 2,\n    "result": 12,\n    "jsonrpc": "2.0"\n  }, {\n    "id": 3,\n    "error": {\n      "code": -32000,\n      "message": "TypeError: unsupported operand type(s) for +: \'int\' and \'str\'"\n    },\n    "jsonrpc": "2.0"\n  }\n]\n```\n\nExample RPC Discover\n\n```json\n{\n  "id": 1,\n  "result": {\n    "openrpc": "1.2.6",\n    "info": {\n      "title": "Demo Server",\n      "version": "1.0.0"\n    },\n    "methods": [\n      {\n        "name": "add",\n        "params": [\n          {\n            "name": "a",\n            "schema": {\n              "type": "number"\n            },\n            "required": true\n          },\n          {\n            "name": "b",\n            "schema": {\n              "type": "number"\n            },\n            "required": true\n          }\n        ],\n        "result": {\n          "name": "result",\n          "schema": {\n            "type": "number"\n          },\n          "required": true\n        }\n      }\n    ],\n    "components": {\n      "schemas": {}\n    }\n  },\n  "jsonrpc": "2.0"\n}\n```\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/openrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
