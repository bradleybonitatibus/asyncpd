import os

import pytest

from asyncpd import APIClient


@pytest.mark.e2e
async def test_main():
    client = APIClient(
        token=os.environ["ASYNCPD_TEST_API_TOKEN"],
    )

    print(await client.abilities.list())
    print(await client.abilities.is_enabled("sso"))
