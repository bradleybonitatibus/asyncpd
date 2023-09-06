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

"""PagerDuty Analytics API resources."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from asyncpd.client import APIClient


@dataclass
class AggregatedMetrics:
    """The Data payload for incident metrics."""

    mean_assignment_count: int | None = None
    mean_engaged_seconds: int | None = None
    mean_engaged_user_count: int | None = None
    mean_seconds_to_engage: int | None = None
    mean_seconds_to_first_ack: int | None = None
    mean_seconds_to_mobilize: int | None = None
    mean_seconds_to_resolve: int | None = None
    range_start: datetime | None = None
    service_id: str | None = None
    service_name: str | None = None
    team_id: str | None = None
    team_name: str | None = None
    total_business_hour_interruptions: int | None = None
    total_engaged_seconds: int | None = None
    total_escalation_count: int | None = None
    total_incident_count: int | None = None
    total_off_hour_interruptions: int | None = None
    total_sleep_hour_interruptions: int | None = None
    total_snoozed_seconds: int | None = None
    up_time_pct: float | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "AggregatedMetrics":
        """Convert a dictionary into an AggregatedMetrics instance."""
        return AggregatedMetrics(**data)


@dataclass
class AggregateDataFilters:
    """User-defined filters to apply to the aggregate incident data analytics endpoint."""

    created_at_start: datetime | None = None
    create_at_end: datetime | None = None
    urgency: Literal["high", "low"] | None = None
    major: bool | None = None
    team_ids: list[str] = field(default_factory=list)
    service_ids: list[str] = field(default_factory=list)
    priority_ids: list[str] = field(default_factory=list)
    priority_names: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialize to dict object."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


class AnalyticsAPI:
    """API resource for interacting with PagerDuty Analytics API."""

    def __init__(self, client: APIClient) -> None:
        """Initialize the Analytics API with a APIClient.

        Args:
            client (APIClient): asyncpd APIClient.
        """
        self.__client = client

    async def __do_aggregate_data_fetch(
        self,
        domain: Literal["all", "services", "teams"] = "all",
        filters: AggregateDataFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> list[AggregatedMetrics]:
        """Get the aggregated data metrics for a given domain."""
        res = await self.__client.request(
            "POST",
            f"/analytics/metrics/incidents/{domain}",
            {"X-EARLY-ACCESS": "analytics-v2"},
            data={
                "filters": None if filters is None else filters.to_dict(),
                "aggregate_unit": aggregate_unit,
                "time_zone": time_zone,
            },
        )

        if res.status_code != 200:
            res.raise_for_status()

        return [AggregatedMetrics.from_dict(d) for d in res.json()["data"]]

    async def get_aggregated_incident_data(
        self,
        filters: AggregateDataFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> list[AggregatedMetrics]:
        """Get the overall incident aggregated data metrics."""
        return await self.__do_aggregate_data_fetch(
            "all", filters, time_zone, aggregate_unit
        )

    async def get_aggregated_service_data(
        self,
        filters: AggregateDataFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> list[AggregatedMetrics]:
        """Get aggregated service data metrics."""
        return await self.__do_aggregate_data_fetch(
            "services", filters, time_zone, aggregate_unit
        )

    async def get_aggregated_team_data(
        self,
        filters: AggregateDataFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> list[AggregatedMetrics]:
        """Get team data metrics."""
        return await self.__do_aggregate_data_fetch(
            "teams", filters, time_zone, aggregate_unit
        )
