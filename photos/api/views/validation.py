from typing import List, Optional


def validate_multiple(key: str, value: str, validators: list) -> List[str]:
    for validator in validators:
        error = validator(value)

        if error is not None:
            return [error.format(key=key)]

    return []


def validate_is_not_none(value: str) -> Optional[str]:
    if value is None:
        return '{key} is required'

    return None


def validate_is_positive_number(value) -> Optional[str]:
    if type(value) is not int:
        return '{key} must be a number'

    if value <= 0:
        return '{key} must be positive'

    return None
