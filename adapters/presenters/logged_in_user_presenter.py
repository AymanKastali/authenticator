from application.dto.logged_in_user_dto import LoggedInUserDTO


class LoggedInUserPresenter:
    @staticmethod
    def to_json(dto: LoggedInUserDTO) -> dict:
        return {
            "uid": dto.uid,
            "email_address": dto.email_address,
            "token": dto.token,
        }
