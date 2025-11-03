from application.services.auth.jwt.auth import JwtAuthService


class LogoutJwtController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    async def execute(self, token: str) -> None:
        await self.service.logout(token)
        return None
