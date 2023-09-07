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
class AggregateAnalyticsResponse:
    """Response wrapper from the aggregate analytics API."""

    time_zone: str
    filters: AnalyticsRequestFilters
    order: str
    order_by: str
    data: list[AggregatedMetrics] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "AggregateAnalyticsResponse":
        """Serialize AggregateAnalyticsResponse dataclass from a dict object."""
        return AggregateAnalyticsResponse(
            time_zone=data["time_zone"],
            filters=AnalyticsRequestFilters.from_dict(data["filters"]),
            order=data["order"],
            order_by=data["order_by"],
            data=[AggregatedMetrics.from_dict(d) for d in data["data"]],
        )


@dataclass
class RawAnalyticsMultipleIncidentsResponse:
    """Response wrapper for raw analytics incident data."""

    first: str
    last: str
    limit: int
    more: bool
    order: str
    order_by: str
    starting_after: datetime | None = None
    filters: AnalyticsRequestFilters | None = None
    ending_before: datetime | None = None
    data: list[RawIncidentData] = field(default_factory=list)

    @classmethod
    def from_dict(self, data: dict) -> "RawAnalyticsMultipleIncidentsResponse":
        """Serialize RawAnalyticsMultipleIncidentsResponse from a dict."""
        return RawAnalyticsMultipleIncidentsResponse(
            first=data["first"],
            last=data["last"],
            limit=data["limit"],
            more=data["more"],
            order=data["order"],
            order_by=data["order_by"],
            starting_after=data["starting_after"],
            filters=AnalyticsRequestFilters.from_dict(data["filters"]),
            ending_before=data["ending_before"],
            data=[RawIncidentData.from_dict(d) for d in data["data"]],
        )


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
    total_incidents_acknowledged: int | None = None
    total_incidents_auto_resolved: int | None = None
    total_incidents_manual_escalated: int | None = None
    total_incidents_reassigned: int | None = None
    total_incidents_timeout_escalated: int | None = None
    total_interruptions: int | None = None
    total_notifications: int | None = None
    total_snoozed_seconds: int | None = None
    up_time_pct: float | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "AggregatedMetrics":
        """Convert a dictionary into an AggregatedMetrics instance."""
        return AggregatedMetrics(**data)


@dataclass
class RawIncidentData:
    """Represents the raw incident data."""

    id: str
    status: str
    created_at: datetime
    assignment_count: int
    business_hour_interruptions: int
    description: str
    engaged_seconds: int
    engaged_user_count: int
    escalation_count: int
    incident_number: int
    major: bool
    off_hour_interruptions: int
    priority_id: str
    priority_name: str
    priority_order: int
    auto_resolved: bool
    urgency: str
    manual_escalation_count: int
    total_interruptions: int
    timeout_escalation_count: int
    reassignment_count: int
    escalation_policy_name: str
    escalation_policy_id: str
    service_name: str
    service_id: str
    total_notifications: int
    snoozed_seconds: int | None = None
    resolved_by_user_name: str | None = None
    resolved_by_user_id: str | None = None
    resolved_at: datetime | None = None
    seconds_to_engage: int | None = None
    seconds_to_first_ack: int | None = None
    seconds_to_mobilize: int | None = None
    seconds_to_resolve: int | None = None
    sleep_hour_interruptions: int | None = None
    snoozed_secondS: int | None = None
    team_id: str | None = None
    team_name: str | None = None
    user_defined_effort_seconds: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "RawIncidentData":
        """Serialize RawIncidentData from a dictionary."""
        return RawIncidentData(**data)


@dataclass
class AnalyticsRequestFilters:
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

    @classmethod
    def from_dict(cls, data: dict) -> "AnalyticsRequestFilters":
        """Serialize AnalyticsRequestFilters object from a dict."""
        return AnalyticsRequestFilters(
            created_at_start=data["created_at_start"],
            create_at_end=data["created_at_end"],
            urgency=data.get("urgency"),
            major=data.get("major"),
            team_ids=data.get("team_ids", []),
            service_ids=data.get("service_ids", []),
            priority_ids=data.get("priority_ids", []),
            priority_names=data.get("priority_names", []),
        )


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
        filters: AnalyticsRequestFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> AggregateAnalyticsResponse:
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

        return AggregateAnalyticsResponse.from_dict(res.json())

    async def get_aggregated_incident_data(
        self,
        filters: AnalyticsRequestFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> AggregateAnalyticsResponse:
        """Get the overall incident aggregated data metrics."""
        return await self.__do_aggregate_data_fetch(
            "all", filters, time_zone, aggregate_unit
        )

    async def get_aggregated_service_data(
        self,
        filters: AnalyticsRequestFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> AggregateAnalyticsResponse:
        """Get aggregated service data metrics."""
        return await self.__do_aggregate_data_fetch(
            "services", filters, time_zone, aggregate_unit
        )

    async def get_aggregated_team_data(
        self,
        filters: AnalyticsRequestFilters | None = None,
        time_zone: str | None = None,
        aggregate_unit: Literal["day", "week", "month"] | None = None,
    ) -> AggregateAnalyticsResponse:
        """Get team data metrics."""
        return await self.__do_aggregate_data_fetch(
            "teams", filters, time_zone, aggregate_unit
        )

    async def get_multiple_raw_incident_data(
        self,
        filters: AnalyticsRequestFilters | None = None,
        limit: int = 20,
        order: str | None = None,
        order_by: str | None = None,
        time_zone: str | None = None,
    ) -> RawAnalyticsMultipleIncidentsResponse:
        """Fetch multiple raw incident data points."""
        res = await self.__client.request(
            "POST",
            "/analytics/raw/incidents",
            headers={
                "X-EARLY-ACCESS": "analytics-v2",
            },
            data={
                "filters": None if filters is None else filters.to_dict(),
                "limit": limit,
                "order": order,
                "order_by": order_by,
                "time_zone": time_zone,
            },
        )

        if res.status_code != 200:
            res.raise_for_status()

        return RawAnalyticsMultipleIncidentsResponse.from_dict(res.json())

    async def get_single_raw_incident_data(
        self, incident_id: str
    ) -> RawIncidentData | None:
        """Get analytics for a single incident.

        Args:
            incident_id (str): Incident ID (e.x. 'P9UMCAE')

        Raises:
            httpx.HTTPStatusError
                when HTTP status is not a 404 or 200

        Returns:
            RawIncidentData | None
                None when the incident_id is not found.
        """
        res = await self.__client.request(
            "GET",
            f"/analytics/raw/incidents/{incident_id}",
            {"X-EARLY-ACCESS": "analytics-v2"},
        )

        if res.status_code == 404:
            return None

        if res.status_code != 200:
            res.raise_for_status()

        return RawIncidentData.from_dict(res.json())
