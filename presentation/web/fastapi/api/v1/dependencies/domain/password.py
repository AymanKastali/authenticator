from domain.config import domain_config
from domain.services.password import PasswordDomainService


def password_domain_service_dependency() -> PasswordDomainService:
    """Provide password service implementation."""
    builder = PasswordDomainService.builder()
    policies = builder.with_config(domain_config.password_config).build()
    return PasswordDomainService(policies)
