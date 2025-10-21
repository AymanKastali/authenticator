from application.dto.logged_in_user_dto import LoggedInUserDTO


class LoggedInUserPresenter:
    @staticmethod
    def to_json(dto: LoggedInUserDTO) -> dict:
        return {
            "uid": dto.uid,
            "email": dto.email,
            "token": dto.token,
        }
