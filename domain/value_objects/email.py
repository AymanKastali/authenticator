from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class EmailVo:
    """
    Immutable Value Object representing an email.
    All validation and normalization must be done in the factory.
    """

    _value: str

    # ----------------- Convenience / Domain Methods -----------------
    def domain(self) -> str:
        return self._value.split("@")[1]

    def username(self) -> str:
        return self._value.split("@")[0]

    @property
    def value(self) -> str:
        return self._value
