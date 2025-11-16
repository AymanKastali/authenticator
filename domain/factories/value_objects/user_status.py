from domain.value_objects.user_status import UserStatusVo


class UserStatusVoFactory:
    @classmethod
    def from_string(cls, status_str: str) -> UserStatusVo:
        status_str = status_str.strip().upper()
        return UserStatusVo[status_str]
