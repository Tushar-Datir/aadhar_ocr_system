import requests


API_URL = "http://127.0.0.1:8000"


def scan_aadhaar(
    front_file,
    back_file=None
):
    """
    Send Aadhaar images to FastAPI OCR API.
    """

    files = {
        "front_image": (
            front_file.name,
            front_file.getvalue(),
            front_file.type
        )
    }

    if back_file is not None:

        files["back_image"] = (
            back_file.name,
            back_file.getvalue(),
            back_file.type
        )

    response = requests.post(
        f"{API_URL}/scan/",
        files=files,
        timeout=120
    )

    response.raise_for_status()

    return response.json()


def get_documents():

    response = requests.get(
        f"{API_URL}/documents/",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def get_document(
    document_id: int
):

    response = requests.get(
        f"{API_URL}/documents/{document_id}",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def delete_document(
    document_id: int
):

    response = requests.delete(
        f"{API_URL}/documents/{document_id}",
        timeout=30
    )

    response.raise_for_status()

    return response.json()