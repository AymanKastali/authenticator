from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(kw_only=True, slots=True)
class PolicyDescriptionDto:
    """
    Generic DTO for any domain policy.
    """

    name: str
    category: str
    parameters: Mapping[str, Any]
