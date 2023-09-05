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

"""Addonds API resources."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from asyncpd.client import APIClient
from asyncpd.models.pagination import ClassicPaginationQuery
from asyncpd.models.service import ServiceReference


class AddonType(str, Enum):
    """Allowed addon types."""

    FULL_PAGE_ADDON = "full_page_addon"
    INCIDENT_SHOW_ADDON = "incident_show_addon"


@dataclass
class NewAddon:
    """New addon inputs."""

    type: AddonType
    name: str
    src: str

    def to_dict(self) -> dict:
        """Convert the dataclass to a dictionary."""
        return {"type": self.type, "name": self.type.value, "src": self.src}


@dataclass
class Addon:
    """PagerDuty addon data model."""

    id: str
    src: str
    type: str
    summary: str | None = None
    name: str | None = None
    self: str | None = None
    html_url: str | None = None
    services: list[ServiceReference] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Addon":
        """Serialize addon from dictionary like object."""
        return Addon(
            id=data["id"],
            src=data["src"],
            type=data["type"],
            summary=data.get("summary"),
            name=data.get("name"),
            self=data.get("self"),
            html_url=data.get("html_url"),
        )


@dataclass
class PaginatedAddon:
    """Data model for paginated addons."""

    limit: int
    offset: int
    more: bool
    total: int | None = None
    addons: list[Addon] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "PaginatedAddon":
        """Serialize paginated addon from dict-like object."""
        return PaginatedAddon(
            limit=data["limit"],
            offset=data["offset"],
            more=data["more"],
            total=data.get("more"),
            addons=[Addon.from_dict(d) for d in data["addons"]],
        )


@dataclass
class AddonUpdateMask:
    """Updatable fields for an addon."""

    name: str
    src: str
    type: AddonType


class AddonsAPI:
    """API resource for addons."""

    def __init__(self, client: APIClient) -> None:
        """Initialize the Addons API resource."""
        self.__client = client

    async def list(
        self,
        query: ClassicPaginationQuery | None = None,
        filter: str | None = None,
        include: list[str] | None = None,
        service_ids: list[str] | None = None,
    ) -> PaginatedAddon:
        """List addons.

        Args:
            query (ClassicPaginationQuery): Pagination query.
            filter (str): Filters addon types.
            service_ids (list[str]): Filters results for given service_ids

        Returns:
            PaginatedAddon

        Raises:
            httpx.HTTPStatusError
        """
        if query is None:
            query = ClassicPaginationQuery()
        res = await self.__client.request(
            "GET",
            "/addons",
            params=[
                (
                    "offset",
                    query.offset,
                ),
                (
                    "limit",
                    query.limit,
                ),
                (
                    "total",
                    query.total,
                ),
                (
                    "filter",
                    filter,
                ),
                (
                    "include[]",
                    include,
                ),
                (
                    "service_ids[]",
                    (",".join(service_ids) if service_ids is not None else None),
                ),
            ],
        )

        if res.status_code != 200:
            res.raise_for_status()

        return PaginatedAddon.from_dict(res.json())

    async def install_addon(
        self,
        new_addon: NewAddon,
    ) -> Addon:
        """Install a new addon."""
        res = await self.__client.request(
            "POST",
            "/addons",
            data=new_addon.to_dict(),
        )

        if res.status_code != 201:
            res.raise_for_status()

        return Addon.from_dict(res.json()["addon"])

    async def get(self, id: str) -> Addon | None:
        """Get an addon by its id.

        Returns:
            Addon | None
                None when the addon is not found.
        """
        res = await self.__client.request(
            "GET",
            f"/addons/{id}",
        )

        if res.status_code == 404:
            return None

        if res.status_code != 200:
            res.raise_for_status()

        return Addon.from_dict(res.json()["addon"])

    async def delete(self, id: str) -> None:
        """Delete an addon."""
        res = await self.__client.request(
            "DELETE",
            f"/addons/{id}",
        )

        if res.status_code != 204:
            res.raise_for_status()

        return None

    async def update(self, id: str, update_mask: AddonUpdateMask) -> Addon:
        """Update an existing addon."""
        res = await self.__client.request(
            "PUT",
            f"/addons/{id}",
            data={
                "addons": {
                    "type": update_mask.type.value,
                    "name": update_mask.name,
                    "src": update_mask.src,
                }
            },
        )

        if res.status_code != 200:
            res.raise_for_status()

        return Addon.from_dict(res.json()["addon"])
