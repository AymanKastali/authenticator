# import re

# from domain.exceptions.domain_errors import PasswordError
# from domain.interfaces.jwt_policy import JwtPolicyInterface
# from domain.value_objects.policy_description import PolicyDescriptionVo


# class JwtExpirationPolicy(JwtPolicyInterface):
#     """Validates basic jwt expiration."""

#     def __init__(
#         self,
#         require_upper=True,
#         require_lower=True,
#         require_digit=True,
#         require_special=True,
#     ):
#         self.require_upper = require_upper
#         self.require_lower = require_lower
#         self.require_digit = require_digit
#         self.require_special = require_special

#     def enforce(self, token: str) -> None:
#         if self.require_upper and not re.search(r"[A-Z]", password):
#             raise PasswordError(
#                 "Password must contain at least one uppercase letter."
#             )
#         if self.require_lower and not re.search(r"[a-z]", password):
#             raise PasswordError(
#                 "Password must contain at least one lowercase letter."
#             )
#         if self.require_digit and not re.search(r"\d", password):
#             raise PasswordError("Password must contain at least one digit.")
#         if self.require_special and not re.search(r"[^A-Za-z0-9]", password):
#             raise PasswordError(
#                 "Password must contain at least one special character."
#             )

#     def describe(self) -> PolicyDescriptionVo:
#         return PolicyDescriptionVo(
#             name="complexity",
#             type="password",
#             parameters={
#                 "require_upper": self.require_upper,
#                 "require_lower": self.require_lower,
#                 "require_digit": self.require_digit,
#                 "require_special": self.require_special,
#             },
#         )
