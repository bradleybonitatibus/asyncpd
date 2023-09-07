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

import logging
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


async def mock_raw_single_incident_data(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "team_id": "PGVXG6U",
            "seconds_to_first_ack": None,
            "escalation_policy_name": "Korabl-Sputnik 3",
            "status": "resolved",
            "sleep_hour_interruptions": 2,
            "manual_escalation_count": 0,
            "urgency": "high",
            "priority_name": "P1",
            "service_id": "PQVUB8D",
            "total_notifications": 2,
            "id": "P9UMCAE",
            "created_at": "2021-01-08T15:36:37",
            "resolved_by_user_id": "PRJ4208",
            "reassignment_count": 0,
            "engaged_user_count": 0,
            "incident_number": 2,
            "assignment_count": 2,
            "resolved_by_user_name": "Brett Willemsen",
            "priority_id": "PITMC5Y",
            "escalation_policy_id": "PCI3U5T",
            "resolved_at": "2021-01-08T15:39:52",
            "business_hour_interruptions": 0,
            "seconds_to_mobilize": None,
            "priority_order": 67108864,
            "seconds_to_engage": None,
            "escalation_count": 0,
            "major": None,
            "description": "Deorbit, engines not cut off as planned",
            "user_defined_effort_seconds": None,
            "auto_resolved": False,
            "team_name": "Space Cosmonauts",
            "service_name": "Korabl-Sputnik 3",
            "timeout_escalation_count": 0,
            "seconds_to_resolve": 195,
            "total_interruptions": None,
            "off_hour_interruptions": 0,
            "engaged_seconds": 0,
            "snoozed_seconds": 0,
        },
    )


async def mock_raw_responses_for_incident(*args, **kwargs) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json={
            "incident_id": "P9UMCAE",
            "limit": 100,
            "order": "asc",
            "order_by": "requested_at",
            "responses": [
                {
                    "requested_at": "2021-01-08T15:36:36",
                    "responded_at": None,
                    "responder_id": "PCY5X6I",
                    "responder_name": "Pcholka",
                    "responder_type": "assigned",
                    "response_status": "pending",
                    "time_to_respond_seconds": None,
                },
                {
                    "requested_at": "2021-01-08T15:36:36",
                    "responded_at": None,
                    "responder_id": "PG7TXJ8",
                    "responder_name": "Mushka",
                    "responder_type": "assigned",
                    "response_status": "pending",
                    "time_to_respond_seconds": None,
                },
            ],
            "time_zone": "Etc/UTC",
        },
    )


async def test_get_aggregated_incident(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_get_aggregate_incident_data):
        res = await client.analytics.get_aggregated_incident_data()
        assert len(res.data) > 0


async def test_get_aggreated_incident_fails(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        with pytest.raises(httpx.HTTPStatusError):
            await client.analytics.get_aggregated_incident_data()


async def test_get_aggregated_service_data(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_get_aggregate_incident_data):
        res = await client.analytics.get_aggregated_service_data()
        assert len(res.data) > 0


async def test_get_aggregated_service_data_fails(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        with pytest.raises(httpx.HTTPStatusError):
            await client.analytics.get_aggregated_service_data()


async def test_get_multiple_raw_data(client: APIClient):
    with mock.patch.object(client, "request", mock_get_raw_data_response):
        res = await client.analytics.get_multiple_raw_incident_data()
        assert len(res.data) > 0


async def test_get_single_raw_data(client: APIClient):
    with mock.patch.object(client, "request", mock_raw_single_incident_data):
        assert await client.analytics.get_single_raw_incident_data("test") is not None


async def test_get_single_raw_data_returns_none(client: APIClient):
    with mock.patch.object(client, "request", mock_not_found):
        assert await client.analytics.get_single_raw_incident_data("test") is None


async def test_get_signle_raw_data_raises(client: APIClient):
    with mock.patch.object(client, "request", mock_invalid_auth):
        with pytest.raises(httpx.HTTPStatusError):
            await client.analytics.get_single_raw_incident_data("test")


async def test_get_raw_responses_for_incident(client: APIClient):
    with mock.patch.object(client, "request", mock_raw_responses_for_incident):
        assert await client.analytics.get_raw_responses_for_incident("test") is not None


async def test_get_raw_responses_for_incident_returns_none(client: APIClient):
    with mock.patch.object(client, "request", mock_not_found):
        assert await client.analytics.get_raw_responses_for_incident("test") is None
