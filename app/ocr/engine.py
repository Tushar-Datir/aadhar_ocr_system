import pytesseract
import numpy as np

from pytesseract import Output


def extract_text(image: np.ndarray) -> str:
    """
    Extract normal OCR text.
    """

    if image is None:
        raise ValueError(
            "Invalid image passed to OCR engine"
        )

    # Good general-purpose document configuration
    config = "--oem 3 --psm 6"

    text = pytesseract.image_to_string(
        image,
        lang="eng",
        config=config
    )

    return text.strip()


def extract_text_data(image: np.ndarray) -> list:
    """
    Extract OCR words with coordinates and confidence.
    """

    if image is None:
        raise ValueError(
            "Invalid image passed to OCR engine"
        )

    configurations = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 11",
        "--oem 3 --psm 3"
    ]

    best_results = []

    for config in configurations:

        data = pytesseract.image_to_data(
            image,
            lang="eng",
            config=config,
            output_type=Output.DICT
        )

        current_results = []

        for i in range(len(data["text"])):

            text = data["text"][i].strip()

            if not text:
                continue

            try:
                confidence = float(
                    data["conf"][i]
                )
            except (ValueError, TypeError):
                confidence = 0.0

            # Ignore extremely low-confidence text
            if confidence < 20:
                continue

            current_results.append({
                "text": text,
                "confidence": round(
                    confidence,
                    2
                ),
                "left": int(
                    data["left"][i]
                ),
                "top": int(
                    data["top"][i]
                ),
                "width": int(
                    data["width"][i]
                ),
                "height": int(
                    data["height"][i]
                )
            })

        if len(current_results) > len(best_results):
            best_results = current_results

    return best_results