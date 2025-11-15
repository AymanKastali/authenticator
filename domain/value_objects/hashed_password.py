from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class HashedPasswordVo:
    _value: str

    @property
    def value(self) -> str:
        return self._value
