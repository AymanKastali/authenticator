from dataclasses import dataclass

@dataclass
class SSOConnectionEntity:
    organization_id: str
    identity_provider: str
    metadata: dict
