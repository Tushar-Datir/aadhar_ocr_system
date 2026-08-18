from sqlalchemy.orm import Session

from app.models.ocr_document import OCRDocument


def create_ocr_document(
    db: Session,
    data: dict
) -> OCRDocument:

    information = data["information"]
    validation = data["validation"]

    document = OCRDocument(
        name=information.get("name"),
        gender=information.get("gender"),
        date_of_birth=information.get("date_of_birth"),
        masked_aadhaar_number=information.get(
            "aadhaar_number"
        ),
        address=information.get("address"),
        is_valid=validation.get(
            "is_valid",
            False
        )
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_all_documents(
    db: Session
) -> list[OCRDocument]:

    return (
        db.query(OCRDocument)
        .order_by(OCRDocument.created_at.desc())
        .all()
    )


def get_document_by_id(
    db: Session,
    document_id: int
) -> OCRDocument | None:

    return (
        db.query(OCRDocument)
        .filter(
            OCRDocument.id == document_id
        )
        .first()
    )

def delete_document(
    db: Session,
    document_id: int
) -> bool:

    document = (
        db.query(OCRDocument)
        .filter(
            OCRDocument.id == document_id
        )
        .first()
    )

    if document is None:
        return False

    db.delete(document)
    db.commit()

    return True