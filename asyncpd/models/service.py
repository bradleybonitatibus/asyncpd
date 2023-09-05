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


"""Service API resource."""


from dataclasses import dataclass


@dataclass
class ServiceReference:
    """Reference to a service."""

    id: str
    type: str
    summary: str
    self: str
    html_url: str

    @classmethod
    def from_dict(cls, data: dict) -> "ServiceReference":
        """Serialize dict into ServiceReference."""
        return ServiceReference(
            id=data["id"],
            type=data["type"],
            summary=data["summary"],
            self=data["self"],
            html_url=data["html_url"],
        )
