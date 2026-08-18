import re
from datetime import datetime


def validate_name(name: str | None) -> bool:
    """Validate extracted name."""

    if not name:
        return False

    name = name.strip()

    # Name should contain only letters and spaces
    if not re.fullmatch(
        r"[A-Za-z]+(?:\s+[A-Za-z]+){1,3}",
        name
    ):
        return False

    return True


def validate_gender(gender: str | None) -> bool:
    """Validate gender."""

    if not gender:
        return False

    return gender.lower() in {
        "male",
        "female",
        "other"
    }


def validate_dob(dob: str | None) -> bool:
    """Validate date of birth."""

    if not dob:
        return False

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y"
    ]

    for date_format in formats:

        try:

            date = datetime.strptime(
                dob,
                date_format
            )

            # DOB shouldn't be in the future
            if date > datetime.now():
                return False

            return True

        except ValueError:
            continue

    return False


def validate_aadhaar(
    aadhaar_number: str | None
) -> bool:
    """
    Validate masked Aadhaar output.

    Expected format:

    XXXX XXXX 1234
    """

    if not aadhaar_number:
        return False

    pattern = (
        r"^XXXX XXXX \d{4}$"
    )

    return bool(
        re.fullmatch(
            pattern,
            aadhaar_number
        )
    )


def validate_document(
    data: dict
) -> dict:
    """
    Validate all extracted fields.
    """

    name = data.get("name")
    gender = data.get("gender")
    dob = data.get("date_of_birth")
    aadhaar = data.get("aadhaar_number")

    validation = {
        "name": validate_name(name),
        "date_of_birth": validate_dob(dob),
        "gender": validate_gender(gender),
        "aadhaar_number": validate_aadhaar(
            aadhaar
        )
    }

    validation["is_valid"] = all(
        validation.values()
    )

    return validation