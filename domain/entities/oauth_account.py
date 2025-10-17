from dataclasses import dataclass

@dataclass
class OAuthAccountEntity:
    provider_name: str
    provider_user_id: str
    access_token: str
    refresh_token: str
