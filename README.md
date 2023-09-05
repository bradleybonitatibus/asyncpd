# asyncpd
Asyncio compatible PagerDuty API client.

[![ci](https://github.com/bradleybonitatibus/asyncpd/actions/workflows/ci.yaml/badge.svg)](https://github.com/bradleybonitatibus/asyncpd/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/asyncpd.svg)](https://badge.fury.io/py/asyncpd)

## Usage

Here is an example usage snippet for interacting with the PagerDuty API
with this package:
```python
import asyncio

from asyncpd import APIClient


async def main():
    client = APIClient(
        token="my_pagerduty_oauth_token",
    )

    print(await client.abilities.list())
    print(await client.abilities.is_enabled("sso"))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```
