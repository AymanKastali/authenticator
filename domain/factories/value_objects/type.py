from domain.value_objects.jwt_type import JwtTypeVo


class JwtTypeVoFactory:
    @classmethod
    def create(cls, type_str: str) -> JwtTypeVo:
        return JwtTypeVo(type_str.strip().upper())
