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
from asyncpd.models import addons

from tests.models.test_helpers import mock_invalid_auth, mock_not_found


async def mock_list_addons(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "addons": [
                {
                    "id": "PKX7619",
                    "type": "full_page_addon_reference",
                    "summary": "Internal Status Page",
                    "self": "https://api.pagerduty.com/addons/PKX7619",
                    "html_url": None,
                    "name": "Internal Status Page",
                    "src": "https://intranet.example.com/status",
                }
            ],
            "limit": 25,
            "offset": 0,
            "more": False,
            "total": None,
        },
    )


async def mock_install_addon(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=201,
        json={
            "addon": {
                "id": "PKX7619",
                "type": "full_page_addon_reference",
                "summary": "Internal Status Page",
                "self": "https://api.pagerduty.com/addons/PKX7619",
                "html_url": None,
                "name": "Internal Status Page",
                "src": "https://intranet.example.com/status",
            }
        },
    )


async def mock_get_addon(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "addon": {
                "id": "PKX7F81",
                "type": "incident_show_addon",
                "name": "Service Runbook",
                "src": "https://intranet.example.com/runbook.html",
                "services": [
                    {
                        "id": "PIJ90N7",
                        "type": "service",
                        "summary": "My Application Service",
                        "self": "https://api.pagerduty.com/services/PIJ90N7",
                        "html_url": "https://subdomain.pagerduty.com/services/PIJ90N7",
                    }
                ],
            }
        },
    )


async def mock_delete_addon(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=204,
    )


async def test_list_addons(client: APIClient):
    with mock.patch.object(client, "request", mock_list_addons):
        resource = addons.AddonsAPI(client)
        ad = await resource.list()
        assert ad.more is False


async def test_list_addon_invalid_auth(client: APIClient):
    with mock.patch.object(client, "request", mock_invalid_auth):
        resource = addons.AddonsAPI(client)
        with pytest.raises(httpx.HTTPStatusError):
            await resource.list()


async def test_install_addon(client: APIClient):
    with mock.patch.object(client, "request", mock_install_addon):
        resource = addons.AddonsAPI(client)
        ad = await resource.install_addon(
            addons.NewAddon(
                type=addons.AddonType.FULL_PAGE_ADDON,
                name="test",
                src="https://test",
            )
        )
        assert ad.id is not None
        assert ad.self is not None


async def test_install_invalid_auth(client: APIClient):
    with mock.patch.object(client, "request", mock_invalid_auth):
        resource = addons.AddonsAPI(client)
        with pytest.raises(httpx.HTTPStatusError):
            await resource.install_addon(
                addons.NewAddon(addons.AddonType.FULL_PAGE_ADDON, "test", "test")
            )


async def test_get_addon(client: APIClient):
    with mock.patch.object(client, "request", mock_get_addon):
        resource = addons.AddonsAPI(client)
        ad = await resource.get("test")
        assert ad is not None
        assert ad.id is not None
        assert ad.services is not None


async def test_get_addon_not_found(client: APIClient):
    with mock.patch.object(client, "request", mock_not_found):
        resource = addons.AddonsAPI(client)
        ad = await resource.get("test")
        assert ad is None


async def test_delete_addon(client: APIClient):
    with mock.patch.object(client, "request", mock_delete_addon):
        res = addons.AddonsAPI(client)
        assert await res.delete("test") is None


async def test_update_addon(client: APIClient):
    with mock.patch.object(client, "request", mock_get_addon):
        resource = addons.AddonsAPI(client)
        addon = await resource.update(
            id="test",
            update_mask=addons.AddonUpdateMask(
                name="test 2",
                src="https://hello",
                type=addons.AddonType.FULL_PAGE_ADDON,
            ),
        )
        assert addon is not None
