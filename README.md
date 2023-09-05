# `asyncpd`

`asyncio` compatible PagerDuty REST API client with `dataclass`-typed response models.

[![ci](https://github.com/bradleybonitatibus/asyncpd/actions/workflows/ci.yaml/badge.svg)](https://github.com/bradleybonitatibus/asyncpd/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/asyncpd.svg)](https://badge.fury.io/py/asyncpd)

## Usage

Here is an example usage snippet for interacting with the PagerDuty API
with this package:
```python
import asyncio

from asyncpd import APIClient


async def main():
    client = APIClient(
        token="my_pagerduty_oauth_token",
    )

    print(await client.abilities.list())
    print(await client.abilities.is_enabled("sso"))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```


## Supported APIs

The following list displays what API resources are available in this package.

- [x] Abilities
- [x] Addons
- [ ] Analytics
- [ ] Audit
- [ ] Automation Actions
- [ ] Paused Incident Reports
- [ ] Business Services
- [ ] Custom Fields
- [ ] Change Events
- [ ] Escalation Policies
- [ ] Event Orchestrations
- [ ] Extension Schemas
- [ ] Extensions
- [ ] Incidents
- [ ] Incident Workflows
- [ ] Licenses
- [ ] Log Entries
- [ ] Maintenance Windows
- [ ] Notifications
- [ ] On-Calls
- [ ] Priorities
- [ ] Response Plays
- [ ] Rulesets
- [ ] Schedules
- [ ] Service Dependencies
- [ ] Services
- [ ] Webhooks
- [ ] Standards
- [ ] Status Dashboards
- [ ] Tags
- [ ] Teams
- [ ] Templates
- [ ] Users
- [ ] Vendors
- [ ] EventsV2
