# from domain.policies.jwt.blacklist import JwtBlacklistPolicy


# class LogoutJwtUseCase:
#     def __init__(self, blacklist_repo):
#         self.blacklist_repo = blacklist_repo
#         self.policy = JwtBlacklistPolicy()

#     def logout(self, jti: str):
#         """Invalidate the token until it naturally expires."""
#         revoked_tokens = self.blacklist_repo.get_revoked_tokens()
#         self.policy.enforce(jti, revoked_tokens)

#         # store token in blacklist with expiration
#         self.blacklist_repo.add_token(jti, expires_in)
