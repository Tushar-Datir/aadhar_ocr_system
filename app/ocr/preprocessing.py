import cv2
import numpy as np


def resize_image(
    image: np.ndarray
) -> np.ndarray:
    """
    Resize image for OCR.
    """

    if image is None:
        raise ValueError(
            "Invalid image"
        )

    height, width = image.shape[:2]

    if width < 1600:

        scale = 1600 / width

        new_width = int(
            width * scale
        )

        new_height = int(
            height * scale
        )

        image = cv2.resize(
            image,
            (
                new_width,
                new_height
            ),
            interpolation=cv2.INTER_CUBIC
        )

    return image


def preprocess_image(
    image: np.ndarray
) -> np.ndarray:
    """
    General preprocessing.
    Kept for future OCR pipelines.
    """

    image = resize_image(
        image
    )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    denoised = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(
        denoised
    )

    processed = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return processed