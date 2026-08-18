import re
import cv2
import pytesseract


# ---------------------------------------------------------
# Common helpers
# ---------------------------------------------------------

def clean_ocr_text(text: str) -> str:
    """Clean OCR output."""

    if not text:
        return ""

    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove repeated blank lines
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# ---------------------------------------------------------
# Name extraction
# ---------------------------------------------------------

def extract_name(text: str):
    """
    Extract person's name from Aadhaar front side.

    Aadhaar may not contain a 'Name:' label,
    so we also look for likely person-name lines.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # ---------------------------------------------
    # First: explicit Name / Naam label
    # ---------------------------------------------

    for line in lines:

        match = re.search(
            r"\b(?:name|naam)\b\s*[:\-]?\s*(.+)",
            line,
            re.IGNORECASE
        )

        if match:

            candidate = match.group(1).strip()

            candidate = re.sub(
                r"^[^A-Za-z]+",
                "",
                candidate
            )

            if is_possible_name(candidate):
                return candidate

    # ---------------------------------------------
    # Second: standalone name
    # ---------------------------------------------

    excluded_words = {
        "government",
        "india",
        "unique",
        "identification",
        "authority",
        "aadhaar",
        "male",
        "female",
        "address",
        "dob",
        "date",
        "birth",
        "nashik",
        "maharashtra",
        "room",
        "number",
        "enrolment",
        "enrollment"
    }

    for line in lines:

        # Remove OCR garbage at beginning/end
        candidate = re.sub(
            r"^[^A-Za-z]+",
            "",
            line
        )

        candidate = re.sub(
            r"[^A-Za-z\s]+$",
            "",
            candidate
        )

        candidate = re.sub(
            r"\s+",
            " ",
            candidate
        ).strip()

        if not is_possible_name(candidate):
            continue

        words = candidate.lower().split()

        # Skip known document words
        if any(
            word in excluded_words
            for word in words
        ):
            continue

        return candidate

    return None


def is_possible_name(text: str) -> bool:
    """Check whether text looks like a person's name."""

    # Remove non alphabetic characters
    cleaned = re.sub(
        r"[^A-Za-z\s]",
        " ",
        text
    )

    cleaned = re.sub(
        r"\s+",
        " ",
        cleaned
    ).strip()

    if not cleaned:
        return False

    words = cleaned.split()

    # Typical name: 2-4 words
    if len(words) < 2 or len(words) > 4:
        return False

    for word in words:

        if not word.isalpha():
            return False

        if len(word) < 2:
            return False

        if len(word) > 20:
            return False

    return True


# ---------------------------------------------------------
# Gender extraction
# ---------------------------------------------------------

def extract_gender(text: str):
    """Extract gender."""

    match = re.search(
        r"\b(FEMALE|MALE|OTHER)\b",
        text,
        re.IGNORECASE
    )

    if not match:
        return None

    gender = match.group(1).lower()

    if gender == "male":
        return "Male"

    if gender == "female":
        return "Female"

    return "Other"


# ---------------------------------------------------------
# DOB extraction
# ---------------------------------------------------------

def extract_dob(text: str):
    """Extract date of birth."""

    patterns = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{2}\.\d{2}\.\d{4}\b"
    ]

    # Prefer DOB-labelled date
    dob_match = re.search(
        r"(?:DOB|Date\s*of\s*Birth)"
        r"\s*[:\-]?\s*"
        r"(\d{2}[/-]\d{2}[/-]\d{4})",
        text,
        re.IGNORECASE
    )

    if dob_match:
        return dob_match.group(1)

    # General date search
    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0)

    return None


# ---------------------------------------------------------
# Aadhaar number extraction
# ---------------------------------------------------------

def extract_aadhaar_number(text: str):
    """
    Extract a 12-digit Aadhaar-like number.

    Returns a masked value for security.
    """

    # ---------------------------------------------
    # Format:
    # 1234 5678 9012
    # ---------------------------------------------

    match = re.search(
        r"(?<!\d)"
        r"(\d{4})[\s\-]+"
        r"(\d{4})[\s\-]+"
        r"(\d{4})"
        r"(?!\d)",
        text
    )

    if match:

        number = (
            match.group(1)
            + match.group(2)
            + match.group(3)
        )

        return f"XXXX XXXX {number[-4:]}"

    # ---------------------------------------------
    # Continuous 12 digits
    # ---------------------------------------------

    match = re.search(
        r"(?<!\d)\d{12}(?!\d)",
        text
    )

    if match:

        number = match.group(0)

        return f"XXXX XXXX {number[-4:]}"

    return None


# ---------------------------------------------------------
# FRONT SIDE
# ---------------------------------------------------------

def front_data(img):
    """
    Extract front-side Aadhaar information.

    Returns:
        name
        gender
        dob
        aadhaar_number
    """

    if img is None:
        raise ValueError(
            "Invalid Aadhaar front image"
        )

    # ---------------------------------------------
    # OCR pass 1 - better for name/layout
    # ---------------------------------------------

    config_name = "--psm 4 --oem 3"

    text_name = pytesseract.image_to_string(
        img,
        lang="eng",
        config=config_name
    )

    # ---------------------------------------------
    # OCR pass 2 - general document OCR
    # ---------------------------------------------

    config_general = "--psm 3 --oem 3"

    text_general = pytesseract.image_to_string(
        img,
        lang="eng",
        config=config_general
    )

    # ---------------------------------------------
    # Combine OCR results
    # ---------------------------------------------

    text = (
        text_name
        + "\n"
        + text_general
    )

    text = clean_ocr_text(text)

    # ---------------------------------------------
    # Extract fields
    # ---------------------------------------------

    name = extract_name(
        text_name
    )

    if not name:
        name = extract_name(
            text_general
        )

    gender = extract_gender(
        text
    )

    dob = extract_dob(
        text
    )

    aadhaar_number = extract_aadhaar_number(
        text
    )

    return (
        name,
        gender,
        dob,
        aadhaar_number
    )


# ---------------------------------------------------------
# BACK SIDE
# ---------------------------------------------------------

def back_data(img):
    """
    Extract address from Aadhaar back side.
    """

    if img is None:
        raise ValueError(
            "Invalid Aadhaar back image"
        )

    # PSM 11 is useful for sparse document text
    config = "--psm 11 --oem 3"

    ocr_text = pytesseract.image_to_string(
        img,
        lang="eng",
        config=config
    )

    ocr_text = clean_ocr_text(
        ocr_text
    )

    if not ocr_text:
        return None

    lines = [
        line.strip()
        for line in ocr_text.splitlines()
        if line.strip()
    ]

    # ---------------------------------------------
    # Find beginning of address
    # ---------------------------------------------

    address_start = None

    for index, line in enumerate(lines):

        if re.search(
            r"\baddress\b",
            line,
            re.IGNORECASE
        ):
            address_start = index
            break

        if re.search(
            r"^\s*To\s*$",
            line,
            re.IGNORECASE
        ):
            address_start = index
            break

        if re.search(
            r"^\s*To\s*:",
            line,
            re.IGNORECASE
        ):
            address_start = index
            break

    # ---------------------------------------------
    # If "Address" wasn't detected,
    # search for a PIN code and use nearby lines
    # ---------------------------------------------

    if address_start is None:

        for index, line in enumerate(lines):

            if re.search(
                r"\b\d{6}\b",
                line
            ):

                start = max(
                    0,
                    index - 4
                )

                address_lines = lines[
                    start:index + 1
                ]

                return " ".join(
                    address_lines
                )

        return None

    # ---------------------------------------------
    # Start after Address / To
    # ---------------------------------------------

    address_lines = []

    first_line = lines[address_start]

    first_line = re.sub(
        r"^\s*(?:Address|To)\s*[:\-]?\s*",
        "",
        first_line,
        flags=re.IGNORECASE
    ).strip()

    if first_line:
        address_lines.append(
            first_line
        )

    # ---------------------------------------------
    # Collect address until PIN code
    # ---------------------------------------------

    for line in lines[address_start + 1:]:

        address_lines.append(
            line
        )

        # Indian PIN code = 6 digits
        if re.search(
            r"\b\d{6}\b",
            line
        ):
            break

    if not address_lines:
        return None

    address = " ".join(
        address_lines
    )

    # Clean excessive spaces
    address = re.sub(
        r"\s+",
        " ",
        address
    ).strip()

    return address


# ---------------------------------------------------------
# MAIN FRONT/BACK PROCESSING
# ---------------------------------------------------------

def extract_aadhaar_data(
    front_img,
    back_img=None
):
    """
    Complete Aadhaar extraction.

    Front:
        Name
        Gender
        DOB
        Aadhaar number

    Back:
        Address
    """

    (
        name,
        gender,
        dob,
        aadhaar_number
    ) = front_data(
        front_img
    )

    address = None

    if back_img is not None:

        address = back_data(
            back_img
        )

    return {
        "name": name,
        "gender": gender,
        "date_of_birth": dob,
        "aadhaar_number": aadhaar_number,
        "address": address
    }