from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True, slots=True)
class PolicyDto:
    """
    Generic DTO for any domain policy.
    """

    name: str
    type: str
    parameters: dict[str, Any]
