import jwt

from adapters.utils.time_utils import (
    expires_after_days,
    expires_after_minutes,
    utc_now,
)
from application.ports.jwt_token_service import JwtTokenServicePort


class JwtService(JwtTokenServicePort):
    def __init__(
        self,
        secret: str,
        access_exp_minutes: int = 15,
        refresh_exp_days: int = 7,
    ):
        self.secret = secret
        self.access_exp = access_exp_minutes
        self.refresh_exp = refresh_exp_days

    def generate_access_token(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "iat": utc_now(),
            "exp": expires_after_minutes(self.access_exp),
            "type": "access",
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def generate_refresh_token(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "iat": utc_now(),
            "exp": expires_after_days(self.refresh_exp),
            "type": "refresh",
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_access_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload.get("type") != "access":
                return None
            return payload["sub"]
        except jwt.PyJWTError:
            return None

    def verify_refresh_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload.get("type") != "refresh":
                return None
            return payload["sub"]
        except jwt.PyJWTError:
            return None
