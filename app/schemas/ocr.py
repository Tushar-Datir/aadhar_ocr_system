from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AadhaarInformation(BaseModel):

    name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    aadhaar_number: Optional[str] = None
    address: Optional[str] = None


class ValidationResult(BaseModel):

    name: bool
    gender: bool
    date_of_birth: bool
    aadhaar_number: bool
    address: Optional[bool] = None
    is_valid: bool


class AadhaarOCRData(BaseModel):

    information: AadhaarInformation
    validation: ValidationResult


class AadhaarOCRResponse(BaseModel):

    success: bool
    data: AadhaarOCRData


class DocumentResponse(BaseModel):

    id: int
    name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    aadhaar_number: Optional[str] = None
    address: Optional[str] = None
    is_valid: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):

    success: bool
    count: int
    documents: list[DocumentResponse]