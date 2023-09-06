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
                    "mean_assignment_count": 1,
                    "mean_engaged_seconds": 366,
                    "mean_engaged_user_count": 1,
                    "mean_seconds_to_engage": 81,
                    "mean_seconds_to_first_ack": 63,
                    "mean_seconds_to_mobilize": 41,
                    "mean_seconds_to_resolve": 380,
                    "range_start": "2020-01-01T00:00:00.000000",
                    "total_business_hour_interruptions": 81,
                    "total_engaged_seconds": 3591,
                    "total_escalation_count": 5,
                    "total_incident_count": 124,
                    "total_off_hour_interruptions": 20,
                    "total_sleep_hour_interruptions": 21,
                    "total_snoozed_seconds": 78,
                }
            ],
            "filters": {
                "create_range_start": "2020-01-01T00:00:00Z",
                "create_range_end": "2020-02-01T00:00:00Z",
            },
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
                    "mean_assignment_count": 1,
                    "mean_engaged_seconds": 366,
                    "mean_engaged_user_count": 1,
                    "mean_seconds_to_engage": 81,
                    "mean_seconds_to_first_ack": 63,
                    "mean_seconds_to_mobilize": 41,
                    "mean_seconds_to_resolve": 380,
                    "service_id": "PPSCXAN",
                    "service_name": "Critical Prod Service 1",
                    "team_id": "P3XUQ75",
                    "team_name": "Engineering",
                    "total_business_hour_interruptions": 81,
                    "total_engaged_seconds": 3591,
                    "total_escalation_count": 5,
                    "total_incident_count": 124,
                    "total_off_hour_interruptions": 20,
                    "total_sleep_hour_interruptions": 21,
                    "total_snoozed_seconds": 78,
                    "up_time_pct": 99.92677595628416,
                },
                {
                    "mean_assignment_count": 1,
                    "mean_engaged_seconds": 366,
                    "mean_engaged_user_count": 1,
                    "mean_seconds_to_engage": 81,
                    "mean_seconds_to_first_ack": 63,
                    "mean_seconds_to_mobilize": 41,
                    "mean_seconds_to_resolve": 380,
                    "service_id": "PPSCXAN",
                    "service_name": "Meme Fetcher Bot",
                    "team_id": "PDN84B1",
                    "team_name": "Marketing",
                    "total_business_hour_interruptions": 81,
                    "total_engaged_seconds": 3591,
                    "total_escalation_count": 5,
                    "total_incident_count": 124,
                    "total_off_hour_interruptions": 20,
                    "total_sleep_hour_interruptions": 21,
                    "total_snoozed_seconds": 78,
                    "up_time_pct": 99.98747723132969,
                },
            ],
            "filters": {
                "created_at_start": "2020-06-17T17:27:27Z",
                "created_at_end": "2020-06-16T17:27:27Z",
            },
            "time_zone": "Etc/UTC",
        },
    )


async def test_get_aggregated_incident(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_get_aggregate_incident_data):
        resource = analytics.AnalyticsAPI(client)
        res = await resource.get_aggregated_incident_data()
        assert len(res) > 0


async def test_get_aggreated_incident_fails(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        resource = analytics.AnalyticsAPI(client)
        with pytest.raises(httpx.HTTPStatusError):
            await resource.get_aggregated_incident_data()


async def test_get_aggregated_service_data(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_get_aggregate_incident_data):
        resource = analytics.AnalyticsAPI(client)
        res = await resource.get_aggregated_service_data()
        assert len(res) > 0


async def test_get_aggregated_service_data_fails(client: APIClient) -> None:
    with mock.patch.object(client, "request", mock_invalid_auth):
        resource = analytics.AnalyticsAPI(client)
        with pytest.raises(httpx.HTTPStatusError):
            await resource.get_aggregated_service_data()
