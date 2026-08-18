import os
import uuid

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.ocr_service import (
    process_front_aadhaar
)

from app.repositories.ocr_repository import (
    create_ocr_document,
    get_all_documents,
    get_document_by_id
)

from app.schemas.ocr import (
    AadhaarOCRResponse,
    DocumentResponse,
    DocumentListResponse
)

from app.repositories.ocr_repository import (
    create_ocr_document,
    get_all_documents,
    get_document_by_id,
    delete_document
)


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="Aadhaar OCR API",
    description=(
        "OCR and information extraction "
        "system for Aadhaar documents"
    ),
    version="1.0.0"
)


# =========================================================
# Configuration
# =========================================================

UPLOAD_DIR = "data/input"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png"
}


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}


# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Aadhaar OCR API is running!",
        "version": "1.0.0"
    }


# =========================================================
# File Validation
# =========================================================

def validate_file(
    file: UploadFile
):
    """
    Validate uploaded image.
    """

    # Check MIME type
    if file.content_type not in ALLOWED_CONTENT_TYPES:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only JPG, JPEG and PNG "
                "images are allowed."
            )
        )

    # Check filename
    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    # Get extension
    extension = os.path.splitext(
        file.filename
    )[1].lower()

    # Check extension
    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail="Invalid file extension."
        )

    return extension


# =========================================================
# Save Uploaded File
# =========================================================

async def save_upload(
    file: UploadFile
) -> str:
    """
    Save uploaded image to data/input.
    """

    extension = validate_file(
        file
    )

    # Generate unique filename
    filename = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Read file
    content = await file.read()

    # Save file
    with open(
        file_path,
        "wb"
    ) as f:

        f.write(content)

    return file_path


# =========================================================
# Scan Aadhaar
# =========================================================

@app.post(
    "/scan/",
    response_model=AadhaarOCRResponse
)
async def scan_aadhaar(
    front_image: UploadFile = File(...),
    back_image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Save front image
    # -----------------------------------------------------

    front_path = await save_upload(
        front_image
    )

    # -----------------------------------------------------
    # Save optional back image
    # -----------------------------------------------------

    back_path = None

    if back_image is not None:

        back_path = await save_upload(
            back_image
        )

    # -----------------------------------------------------
    # OCR Processing
    # -----------------------------------------------------

    try:

        result = process_front_aadhaar(
            front_path,
            back_path
        )

        # -------------------------------------------------
        # Save OCR result to PostgreSQL
        # -------------------------------------------------

        create_ocr_document(
            db,
            result
        )

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        # Rollback database transaction
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# Get All Documents
# =========================================================

@app.get(
    "/documents/",
    response_model=DocumentListResponse
)
def get_documents(
    db: Session = Depends(get_db)
):

    documents = get_all_documents(
        db
    )

    return {
        "success": True,
        "count": len(documents),
        "documents": documents
    }


# =========================================================
# Get Document By ID
# =========================================================

@app.get(
    "/documents/{document_id}",
    response_model=DocumentResponse
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = get_document_by_id(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@app.delete(
    "/documents/{document_id}"
)
def remove_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_document(
        db,
        document_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "success": True,
        "message": "Document deleted successfully",
        "document_id": document_id
    }