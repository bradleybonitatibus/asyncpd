# asyncpd
Asyncio compatible PagerDuty API client.

[![ci](https://github.com/bradleybonitatibus/asyncpd/actions/workflows/ci.yaml/badge.svg)](https://github.com/bradleybonitatibus/asyncpd/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/asyncpd.svg)](https://badge.fury.io/py/asyncpd)

## Usage

Here is an example usage snippet for interacting with the PagerDuty API
with this package:
```python
from asyncpd import APIClient
from asyncpd.models.abilities import AbilitiesAPI


client = APIClient(
    token="my_pagerduty_oauth_token",
)

abilities_api = AbilitiesAPI(client)
print(await abilities_api.list())
print(abilities_api.is_enabled("sso"))
```
