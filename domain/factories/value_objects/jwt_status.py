from domain.value_objects.jwt_status import JwtStatusVo


class JwtStatusVoFactory:
    @classmethod
    def from_string(cls, status_str: str) -> JwtStatusVo:
        return JwtStatusVo(status_str.strip().upper())
