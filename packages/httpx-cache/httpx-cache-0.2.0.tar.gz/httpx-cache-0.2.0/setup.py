# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['httpx_cache',
 'httpx_cache.cache',
 'httpx_cache.serializer',
 'httpx_cache.transport']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.4.0,<4.0.0',
 'attrs>=21.2.0,<22.0.0',
 'fasteners>=0.16.3,<0.17.0',
 'httpx>=0.21.1,<0.22.0',
 'msgpack>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'httpx-cache',
    'version': '0.2.0',
    'description': 'Simple caching transport for httpx.',
    'long_description': '# HTTPX-CACHE\n\n[![codecov](https://codecov.io/gh/bendidi/httpx-cache/branch/main/graph/badge.svg?token=FHHRA6F17X)](https://codecov.io/gh/bendidi/httpx-cache)\n\nNote: Early development / alpha, use at your own risk.\n\nhttpx-cache is yet another implementation/port is a port of the caching algorithms in httplib2 for use with httpx Transport object.\n\nIt is is heavily insipired by:\n\n- [https://github.com/ionrock/cachecontrol](https://github.com/ionrock/cachecontrol)\n- [https://github.com/johtso/httpx-caching](https://github.com/johtso/httpx-caching)\n\nThis project supports the latest version of httpx (at of the time of writing): `httpx@0.21.1`, when `httpx` releases a v1 version, the update should be straithforward for this project.\n\n## Installation\n\nUsing pip:\n\n```sh\npip install httpx-cache\n```\n\nUsing poetry:\n\n```sh\npoetry add httpx-cache\n```\n\n## Features\n\n- In memory dict cache store\n- Support for cache-controle headers\n- Sync cache transport for httpx\n- Async cache transport for httpx\n\n## Quickstart\n\nThe lib provides an `httpx` compliant transport that you can use instead of the the defult one when creating your `httpx` client:\n\n```py\nimport httpx\n\nfrom httpx_cache import CacheControlTransport\n\nwith httpx.Client(transport=CacheControlTransport()) as client:\n  response = client.get("https://httpbin.org/get")\n\n  # the response is effectively cached, calling teh same request with return a response from the cache\n\n  response2 = client.get("https://httpbin.org/get")\n```\n\nYou can also wrap an existing transport with `CacheControlTransport`. The `CacheControlTransport` will use the existing transport for making the request call and then cach the result if it satisfies the cache-control headers.\n\n```py\nimport httpx\n\nfrom httpx_cache import CacheControlTransport\n\nmy_transport = httpx.HTTPTransport(http2=True, verify=False)\n\nwith httpx.Client(transport=CacheControlTransport(transport=my_transport)) as client:\n  response = client.get("https://httpbin.org/get")\n\n  # the response is effectively cached, calling teh same request with return a response from the cache\n\n  response2 = client.get("https://httpbin.org/get")\n```\n\n## Examples\n\n more examples in [./examples](./examples).\n\n## TODO\n\n- [ ] support etags\n- [ ] support cache expiry dates\n- [ ] support file cach\n- [ ] support redis (sync/async) cache\n',
    'author': 'Ouail Bendidi',
    'author_email': 'ouail.bendidi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bendidi/httpx-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
