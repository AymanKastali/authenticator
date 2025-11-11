# from uuid import UUID

# from domain.entities.user import UserEntity
# from domain.services.user.authenticate_user import AuthenticateUser
# from domain.services.user.manage_password import ManageUserPassword
# from domain.services.user.manage_status import ManageUserStatus
# from domain.services.user.query_user import QueryUser
# from domain.services.user.register_user import RegisterUser
# from domain.value_objects.email import EmailVo
# from domain.value_objects.hashed_password import HashedPasswordVo
# from domain.value_objects.identifiers import UUIDVo


# class UserAppService:
#     """
#     Application service orchestrating user use cases.
#     Delegates domain logic to specific domain services.
#     """

#     def __init__(
#         self,
#         registration: RegisterUser,
#         authentication: AuthenticateUser,
#         status_management: ManageUserStatus,
#         password_management: ManageUserPassword,
#         query_user,
#     ):
#         self._registration = registration
#         self._authentication = authentication
#         self._status_management = status_management
#         self._password_management = password_management
#         self._query_user = query_user

#     # -------------------- Registration --------------------
#     async def register_local_user(self, email: str, password: str) -> UserDto:
#         email_vo = EmailVo.from_string(email)
#         hashed_pw = HashedPasswordVo.create(password, self._password_policies)
#         user: UserEntity = await self._registration.register_local_user(
#             email_vo, hashed_pw
#         )
#         return UserDto.from_entity(user)

#     async def register_external_user(self, email: str) -> UserDto:
#         email_vo = EmailVo.from_string(email)
#         user: UserEntity = await self._registration.register_external_user(
#             email_vo
#         )
#         return UserDto.from_entity(user)

#     # -------------------- Authentication --------------------
#     async def authenticate_user(self, email: str, password: str) -> UserDto:
#         email_vo = EmailVo.from_string(email)
#         user: UserEntity = await self._authentication.authenticate_user(
#             email_vo, password
#         )
#         return UserDto.from_entity(user)

#     # -------------------- Status Management --------------------
#     async def activate_user(self, user_id: UUID) -> UserDto:
#         uid_vo = UUIDVo.from_string(str(user_id))
#         await self._status_management.activate_user(uid_vo)
#         user = await self._query.get_user_by_id(uid_vo)
#         return UserDto.from_entity(user)

#     async def deactivate_user(self, user_id: UUID) -> UserDto:
#         uid_vo = UUIDVo.from_string(str(user_id))
#         await self._status_management.deactivate_user(uid_vo)
#         user = await self._query.get_user_by_id(uid_vo)
#         return UserDto.from_entity(user)

#     async def mark_user_verified(self, user_id: UUID) -> UserDto:
#         uid_vo = UUIDVo.from_string(str(user_id))
#         await self._status_management.mark_user_verified(uid_vo)
#         user = await self._query.get_user_by_id(uid_vo)
#         return UserDto.from_entity(user)

#     # -------------------- Password Management --------------------
#     async def change_user_password(self, user_id: UUID, new_password: str):
#         uid_vo = UUIDVo.from_string(str(user_id))
#         hashed_pw = HashedPasswordVo.create(new_password)
#         await self._password_management.change_password(uid_vo, hashed_pw)

#     # -------------------- Queries --------------------
#     async def get_user_by_email(self, email: str) -> UserDto | None:
#         user = await self._query.get_user_by_email(EmailVo.from_string(email))
#         return UserDto.from_entity(user) if user else None

#     async def get_user_by_id(self, user_id: UUID) -> UserDto | None:
#         uid_vo = UUIDVo.from_string(str(user_id))
#         user = await self._query.get_user_by_id(uid_vo)
#         return UserDto.from_entity(user) if user else None

#     async def get_all_users(self) -> list[UserDto]:
#         users = await self._query.get_all_users()
#         return [UserDto.from_entity(u) for u in users]
