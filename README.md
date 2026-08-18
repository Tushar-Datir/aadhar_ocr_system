# Aadhaar OCR System

An AI-powered document processing system that extracts structured information from Aadhaar card images using Optical Character Recognition (OCR), image preprocessing, and document analysis techniques.

The system is designed to simplify the extraction of important information from Aadhaar documents while reducing manual data entry.

---

## 📌 Project Overview

Manually entering information from identity documents can be time-consuming and error-prone.

The Aadhaar OCR System automates this process by accepting an Aadhaar card image, preprocessing the image to improve quality, detecting and extracting text using OCR, and converting the extracted information into structured fields.

### Processing Pipeline

```text
Aadhaar Image
      │
      ▼
Image Upload
      │
      ▼
Image Preprocessing
      │
      ├── Noise Removal
      ├── Grayscale Conversion
      ├── Thresholding
      ├── Image Enhancement
      ├── Alignment / Deskewing
      └── Contour / Layout Analysis
      │
      ▼
OCR Processing
      │
      ▼
Raw Text Extraction
      │
      ▼
Text Cleaning & Processing
      │
      ▼
Field Extraction
      │
      ├── Name
      ├── Date of Birth
      ├── Gender
      ├── Aadhaar Number
      └── Address
      │
      ▼
Validation
      │
      ▼
Structured Output

🚀 Features
📷 Upload Aadhaar card images
🔍 OCR-based text extraction
🖼️ Image preprocessing using OpenCV
🧹 Noise removal
⚫ Grayscale conversion
🔲 Thresholding and binarization
📐 Image alignment and deskewing
📄 Document layout analysis
🔎 Text region detection
🧠 Intelligent field extraction
🪪 Aadhaar number detection
👤 Name extraction
📅 Date of birth extraction
⚧ Gender extraction
📍 Address extraction
✅ Extracted data validation
📊 Structured JSON output
🌐 Web-based interface
🔌 API-based backend architecture
🧪 Testing support
🔐 Sensitive-document handling considerations
🛠️ Technologies Used
Programming Language
Python
Computer Vision
OpenCV
NumPy
OCR
Tesseract OCR
pytesseract
Backend
FastAPI
Uvicorn
Pydantic
Frontend
Streamlit
Data Processing
Regular Expressions
NumPy
Python Standard Library
Development Tools
Git
GitHub
Visual Studio Code
Python Virtual Environment

📂 Project Structure

aadhar_ocr_system/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── ...
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── ocr.py
│   │   ├── preprocessing.py
│   │   └── extraction.py
│   │
│   ├── utils/
│   │   └── ...
│   │
│   └── ...
│
├── frontend/
│   ├── main.py
│   └── ...
│
├── tests/
│   ├── test_ocr.py
│   └── ...
│
├── data/
│   └── sample/
│
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE

How It Works
1. Image Upload

The user uploads an Aadhaar card image through the web interface.

Supported image formats may include:

JPG
JPEG
PNG
2. Image Preprocessing

Raw document images can contain:

Noise
Shadows
Uneven lighting
Low contrast
Skewed text
Blurred regions
Background artifacts

OpenCV is used to improve the image before OCR.

Typical preprocessing operations include:

Original Image
      ↓
Resize
      ↓
Grayscale
      ↓
Noise Removal
      ↓
Contrast Enhancement
      ↓
Thresholding
      ↓
Deskew / Alignment
      ↓
OCR-ready Image
3. OCR

The processed image is passed to the OCR engine.

OCR converts the visual characters into machine-readable text.

Example:

Image
  ↓
OCR
  ↓
"Name: XXXXX XXXXX
 DOB: XX/XX/XXXX
 Gender: Male
 ..."
4. Text Processing

The raw OCR output may contain:

Extra spaces
Incorrect characters
Line breaks
OCR noise
Missing characters

Regular expressions and text-processing techniques are used to clean and analyze the result.

5. Field Extraction

The system attempts to identify important Aadhaar fields.

Example:

{
    "name": "Example Name",
    "date_of_birth": "01/01/2000",
    "gender": "Male",
    "aadhaar_number": "XXXX XXXX XXXX",
    "address": "Example Address"
}

Sensitive information should be masked when displaying or storing real Aadhaar data.

--Running the Application--

Start FastAPI Backend

From the project root:

uvicorn app.main:app --reload

The API will normally be available at:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
Start Streamlit Frontend

Open another terminal:

venv\Scripts\activate

Then:

streamlit run frontend/main.py

The Streamlit application will open in the browser.