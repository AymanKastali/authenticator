from .auth_containers.jwt_auth_container import JwtAuthContainer
from .feature_containers.auth_feature_container import AuthFeatureContainer
from .feature_containers.user_feature_container import UserFeatureContainer

jwt_auth_container = JwtAuthContainer()
feature_user_container = UserFeatureContainer()
feature_auth_container = AuthFeatureContainer(
    jwt_service=jwt_auth_container.jwt_service
)
