from domain.factories.value_objects.header_algorithm import (
    JwtHeaderAlgorithmVoFactory,
)
from domain.value_objects.jwt_header import _HEADER_TYPE, JwtHeaderVo


class JwtHeaderVoFactory:
    """Factory responsible for ALL JwtHeaderVo validation & normalization."""

    # =============================================
    #                   PUBLIC API
    # =============================================
    @classmethod
    def create(
        cls,
        algorithm_str: str,
        typ: str = _HEADER_TYPE,
        kid: str | None = None,
    ) -> JwtHeaderVo:
        normalized_typ = cls._normalize_typ(typ)
        normalized_kid = cls._normalize_kid(kid)

        cls._enforce_valid_typ(normalized_typ)
        cls._enforce_valid_kid(normalized_kid)

        alg_vo = JwtHeaderAlgorithmVoFactory.from_string(algorithm_str)

        return JwtHeaderVo(
            alg=alg_vo,
            typ=_HEADER_TYPE,
            kid=normalized_kid,
        )

    @classmethod
    def from_dict(cls, data: dict) -> JwtHeaderVo:
        return cls.create(
            algorithm_str=data["alg"],
            typ=data.get("typ", _HEADER_TYPE),
            kid=data.get("kid"),
        )

    # =============================================
    #            MINI NORMALIZATION HELPERS
    # =============================================
    @staticmethod
    def _normalize_typ(value: str) -> str:
        return value.strip().upper() if isinstance(value, str) else value

    @staticmethod
    def _normalize_kid(value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    # =============================================
    #              MINI VALIDATION HELPERS
    # =============================================
    @staticmethod
    def _enforce_valid_typ(value: str) -> None:
        if value != _HEADER_TYPE:
            raise ValueError(f"Invalid JWT 'typ': {value}")

    @staticmethod
    def _enforce_valid_kid(value: str | None) -> None:
        if value is None:
            return
        if not value:
            raise ValueError("kid cannot be empty or whitespace")
