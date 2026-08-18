import cv2

from app.ocr.preprocessing import resize_image
from app.ocr.extractor import front_data, back_data
from app.ocr.validator import validate_document


def process_front_aadhaar(
    front_image_path: str,
    back_image_path: str | None = None
) -> dict:

    # -----------------------------------------
    # Load front image
    # -----------------------------------------

    front_image = cv2.imread(
        front_image_path
    )

    if front_image is None:
        raise ValueError(
            f"Unable to load front image: "
            f"{front_image_path}"
        )

    front_image = resize_image(
        front_image
    )

    # -----------------------------------------
    # Extract front information
    # -----------------------------------------

    (
        name,
        gender,
        dob,
        aadhaar_number
    ) = front_data(
        front_image
    )

    # -----------------------------------------
    # Prepare result
    # -----------------------------------------

    extracted_data = {
        "name": name,
        "gender": gender,
        "date_of_birth": dob,
        "aadhaar_number": aadhaar_number,
        "address": None
    }

    # -----------------------------------------
    # Process back image if provided
    # -----------------------------------------

    if back_image_path:

        back_image = cv2.imread(
            back_image_path
        )

        if back_image is None:
            raise ValueError(
                f"Unable to load back image: "
                f"{back_image_path}"
            )

        back_image = resize_image(
            back_image
        )

        address = back_data(
            back_image
        )

        extracted_data["address"] = address

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    validation_data = {
        "name": extracted_data["name"],
        "gender": extracted_data["gender"],
        "date_of_birth": extracted_data["date_of_birth"],
        "aadhaar_number": extracted_data["aadhaar_number"]
    }

    validation = validate_document(
        validation_data
    )

    # Address validation only when supplied
    if back_image_path:

        validation["address"] = bool(
            extracted_data["address"]
        )

    return {
        "information": extracted_data,
        "validation": validation
    }