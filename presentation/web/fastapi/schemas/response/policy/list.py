from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict


class PolicySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    parameters: Mapping[str, Any]


class PoliciesResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category: str
    policies: list[PolicySchema]
