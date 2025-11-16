from domain.value_objects.jwt_status import JwtStatusVo


class JwtStatusVoFactory:
    @classmethod
    def from_string(cls, status_str: str) -> JwtStatusVo:
        status_str = status_str.strip().upper()
        return JwtStatusVo[status_str]
