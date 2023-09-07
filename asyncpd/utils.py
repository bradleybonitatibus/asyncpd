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

"""Utilities module."""


from datetime import datetime


def parse_pd_datetime_format(ds: str) -> datetime:
    """Parse datetime objects.

    PagerDuty (specifically, the Analytics API) has mixed date strings and
    supports the following date-string format: "%Y-%m-%dT%H:%M:%S".
    If the datestring ends with `Z`, the format string will be updated.

    Args:
        ds (str): Date string.

    Returns:
        datetime.datetime
    """
    fmt = "%Y-%m-%dT%H:%M:%S"

    if ds.endswith("Z"):
        fmt = f"{fmt}Z"

    return datetime.strptime(ds, fmt)
