from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class PasswordPolicyConfigDto:
    min_length: int
    max_length: int
    require_upper: bool
    require_lower: bool
    require_digit: bool
    require_special: bool
