from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class PolicyDescriptionVo:
    name: str
    type: str
    parameters: Mapping[str, Any]
