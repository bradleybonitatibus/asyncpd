# Copyright 2023 Bradley Bonitatibus

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Tests for httpx adapter client."""


import os
from asyncpd.client import APIClient
from asyncpd.models.abilities import AbilitiesAPI
from asyncpd.models.addons import AddonsAPI
from asyncpd.models.analytics import AnalyticsAPI


async def test_client_request() -> None:
    c = APIClient(
        token="test",
    )
    res = await c.request("GET", "/abilities")
    assert res.status_code == 401

    c = APIClient(
        token=os.environ["ASYNCPD_TEST_API_TOKEN"],
    )

    res = await c.request("GET", "/health")
    assert res.status_code == 200
    await c.aclose()


async def test_client_api_resource_properties():
    client = APIClient("test")
    assert isinstance(client.abilities, AbilitiesAPI)
    assert isinstance(client.addons, AddonsAPI)
    assert isinstance(client.analytics, AnalyticsAPI)
