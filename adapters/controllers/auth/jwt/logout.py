from application.services.auth.jwt import JwtAuthService


class LogoutJwtController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    def execute(self, token: str) -> None:
        self.service.logout(token)
        return None
