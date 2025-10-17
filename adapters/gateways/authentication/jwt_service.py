from datetime import datetime, timedelta, timezone

import jwt

from application.ports.token_service import TokenServicePort


class JwtService(TokenServicePort):
    def __init__(self, secret: str, expiration_minutes: int = 60):
        self.secret = secret
        self.expiration_minutes = expiration_minutes

    def generate_token(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.expiration_minutes),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.PyJWTError:
            return None
