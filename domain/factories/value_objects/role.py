from domain.value_objects.role import RoleVo


class RoleVoFactory:
    @classmethod
    def from_string(cls, role_str: str) -> RoleVo:
        return RoleVo(role_str.strip().upper())
