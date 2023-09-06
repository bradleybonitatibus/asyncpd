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

"""Analytics API tests."""

from unittest import mock

import httpx
import pytest

from asyncpd.client import APIClient
from asyncpd.models import analytics

from tests.models.test_helpers import mock_invalid_auth, mock_not_found


async def mock_get_aggregate_incident_data(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "aggregate_unit": "day",
            "data": [
                {
                    "mean_assignment_count": 2,
                    "mean_engaged_seconds": 0,
                    "mean_engaged_user_count": 0,
                    "mean_seconds_to_engage": None,
                    "mean_seconds_to_first_ack": None,
                    "mean_seconds_to_mobilize": None,
                    "mean_seconds_to_resolve": 195,
                    "range_start": "2021-01-08T00:00:00",
                    "total_business_hour_interruptions": 0,
                    "total_engaged_seconds": 0,
                    "total_escalation_count": 0,
                    "total_incident_count": 1,
                    "total_incidents_acknowledged": 0,
                    "total_incidents_auto_resolved": 0,
                    "total_incidents_manual_escalated": 0,
                    "total_incidents_reassigned": 0,
                    "total_incidents_timeout_escalated": 0,
                    "total_interruptions": 2,
                    "total_notifications": 2,
                    "total_off_hour_interruptions": 0,
                    "total_sleep_hour_interruptions": 2,
                    "total_snoozed_seconds": 0,
                }
            ],
            "filters": {
                "created_at_end": "2021-01-31T05:00:00Z",
                "created_at_start": "2021-01-01T05:00:00Z",
                "major": True,
                "service_ids": ["PQVUB8D", "PU2D9X3"],
                "team_ids": ["PGVXG6U", "PNVU4U4"],
                "urgency": "high",
            },
            "order": "desc",
            "order_by": "total_incident_count",
            "time_zone": "Etc/UTC",
        },
    )


async def mock_get_aggregate_service_data(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "aggregate_unit": "week",
            "data": [
                {
                    "mean_assignment_count": 2,
                    "mean_engaged_seconds": 0,
                    "mean_engaged_user_count": 0,
                    "mean_seconds_to_engage": None,
                    "mean_seconds_to_first_ack": None,
                    "mean_seconds_to_mobilize": None,
                    "mean_seconds_to_resolve": 195,
                    "range_start": "2021-01-04T00:00:00",
                    "service_id": "PQVUB8D",
                    "service_name": "Korabl-Sputnik 3",
                    "team_id": "PGVXG6U",
                    "team_name": "Space Cosmonauts",
                    "total_business_hour_interruptions": 0,
                    "total_engaged_seconds": 0,
                    "total_escalation_count": 0,
                    "total_incident_count": 1,
                    "total_incidents_acknowledged": 0,
                    "total_incidents_auto_resolved": None,
                    "total_incidents_manual_escalated": 0,
                    "total_incidents_reassigned": 0,
                    "total_incidents_timeout_escalated": 0,
                    "total_interruptions": 2,
                    "total_notifications": 2,
                    "total_off_hour_interruptions": 0,
                    "total_sleep_hour_interruptions": 2,
                    "total_snoozed_seconds": 0,
                    "up_time_pct": 100,
                }
            ],
            "filters": {
                "created_at_end": "2021-01-31T05:00:00Z",
                "created_at_start": "2021-01-01T05:00:00Z",
                "major": True,
                "priority_ids": ["PITMC5Y", "PEHBBT8"],
                "service_ids": ["PQVUB8D", "PU2D9X3"],
                "team_ids": ["PGVXG6U", "PNVU4U4"],
                "urgency": "high",
            },
            "order": "desc",
            "order_by": "total_incident_count",
            "time_zone": "Etc/UTC",
        },
    )


async def mock_get_raw_data_response(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "data": [
                {
                    "sleep_hour_interruptions": 2,
                    "status": "resolved",
                    "resolved_at": "2021-01-08T15:39:52",
                    "incident_number": 2,
                    "seconds_to_resolve": 195,
                    "created_at": "2021-01-08T15:36:37",
                    "priority_name": "P1",
                    "manual_escalation_count": 0,
                    "team_id": "PGVXG6U",
                    "id": "P9UMCAE",
                    "total_interruptions": 2,
                    "escalation_policy_name": "Korabl-Sputnik 3",
                    "engaged_seconds": 0,
                    "priority_order": 67108864,
                    "off_hour_interruptions": 0,
                    "escalation_count": 0,
                    "service_id": "PQVUB8D",
                    "auto_resolved": False,
                    "timeout_escalation_count": 0,
                    "reassignment_count": 0,
                    "seconds_to_mobilize": None,
                    "seconds_to_first_ack": None,
                    "escalation_policy_id": "PCI3U5T",
                    "major": None,
                    "resolved_by_user_name": "Brett Willemsen",
                    "user_defined_effort_seconds": None,
                    "service_name": "Korabl-Sputnik 3",
                    "total_notifications": 2,
                    "description": "Deorbit, engines not cut off as planned",
                    "assignment_count": 2,
                    "snoozed_seconds": 0,
                    "business_hour_interruptions": 0,
                    "resolved_by_user_id": "PRJ4208",
                    "urgency": "high",
                    "engaged_user_count": 0,
                    "seconds_to_engage": None,
                    "priority_id": "PITMC5Y",
                    "team_name": "Space Cosmonauts",
                }
            ],
            "ending_before": None,
            "filters": {
                "created_at_end": "2021-01-31T05:00:00Z",
                "created_at_start": "2021-01-01T05:00:00Z",
                "major": True,
                "priority_names": ["P1", "P2"],
                "service_ids": ["PQVUB8D", "PU2D9X3"],
                "team_ids": ["PGVXG6U", "PNVU4U4"],
                "urgency": "high",
            },
            "first": "eyJpZCI6IlA5VU1DQUUiLCJvcmRlcl9ieSI6ImNyZWF0ZWRfYXQiLCJ2YWx1ZSI6IjIwMjEtMDEtMDhUMTU6MzY6MzcifQ==",
            "last": "eyJpZCI6IlA5VU1DQUUiLCJvcmRlcl9ieSI6ImNyZWF0ZWRfYXQiLCJ2YWx1ZSI6IjIwMjEtMDEtMDhUMTU6MzY6MzcifQ==",
            "limit": 20,
            "more": False,
            "order": "desc",
            "order_by": "created_at",
            "starting_after": None,
            "time_zone": "Etc/UTC",
        },
    )


async def test_get_aggregated_incident(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_get_aggregate_incident_data):
        resource = analytics.AnalyticsAPI(client)
        res = await resource.get_aggregated_incident_data()
        assert len(res.data) > 0


async def test_get_aggreated_incident_fails(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        resource = analytics.AnalyticsAPI(client)
        with pytest.raises(httpx.HTTPStatusError):
            await resource.get_aggregated_incident_data()


async def test_get_aggregated_service_data(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_get_aggregate_incident_data):
        resource = analytics.AnalyticsAPI(client)
        res = await resource.get_aggregated_service_data()
        assert len(res.data) > 0


async def test_get_aggregated_service_data_fails(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        resource = analytics.AnalyticsAPI(client)
        with pytest.raises(httpx.HTTPStatusError):
            await resource.get_aggregated_service_data()


async def test_get_multiple_raw_data(client: APIClient):
    with mock.patch.object(client, "request", mock_get_raw_data_response):
        resource = analytics.AnalyticsAPI(client)
        res = await resource.get_multiple_raw_incident_data()
        assert len(res.data) > 0
