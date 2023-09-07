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


from unittest import mock

import httpx
import pytest

from asyncpd.client import APIClient
from asyncpd.models import abilities

from tests.models.test_helpers import mock_invalid_auth


async def mock_list_abilities(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "abilities": [
                "sso",
                "advanced_reports",
            ]
        },
    )


async def mock_enabled_true(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=204,
    )


async def mock_enabled_false(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=402,
    )


async def test_list_abilities(client: APIClient) -> None:
    with mock.patch.object(
        client,
        "request",
        mock_list_abilities,
    ):
        all_abilities = await client.abilities.list()
        assert len(all_abilities) > 0


async def test_list_abilities_no_auth(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        with pytest.raises(httpx.HTTPStatusError):
            assert await client.abilities.list()


async def test_abilities_is_enabled_true(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_enabled_true):
        assert await client.abilities.is_enabled("teams") is True


async def test_abilities_is_enabled_no_auth(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        with pytest.raises(httpx.HTTPStatusError):
            assert await client.abilities.is_enabled("teams") is True


async def test_abilities_is_enabled_false(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_enabled_false):
        assert await client.abilities.is_enabled("sso") is False
