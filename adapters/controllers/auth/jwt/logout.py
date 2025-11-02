from application.services.auth.jwt.facade import JwtAuthFacade


class LogoutJwtController:
    def __init__(self, service: JwtAuthFacade):
        self.service = service

    async def execute(self, token: str) -> None:
        await self.service.logout(token)
        return None
