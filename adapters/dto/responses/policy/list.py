from typing import Any

from pydantic import BaseModel, ConfigDict


class PoliciesOutDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    type: str
    parameters: dict[str, Any]
