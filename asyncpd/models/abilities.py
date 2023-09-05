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

"""Abilities resource."""
from __future__ import annotations

from typing import List

from asyncpd.client import APIClient

Abilities = List[str]
"""Type alias for abilities resource."""


class AbilitiesAPI:
    """Abilities API resource."""

    def __init__(self, client: APIClient) -> None:
        """Initialize the Abilities API resource."""
        self.__client = client

    async def list(self) -> Abilities:
        """List the enabled abilities in your account."""
        res = await self.__client.request(
            method="GET",
            endpoint="/abilities",
        )

        if not res.status_code == 200:
            res.raise_for_status()

        data: dict = res.json()

        return data.get("abilities", [])

    async def is_enabled(self, ability: str) -> bool:
        """Indicates if an ability is enabled.

        Raises:
            httpx.HTTPStatusError
                when unexpected HTTP error occurs.
        """
        res = await self.__client.request(
            "GET",
            f"/abilities/{ability}",
        )
        if res.status_code not in (204, 402):
            res.raise_for_status()

        return res.status_code == 204
