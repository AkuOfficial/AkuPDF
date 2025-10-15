# AkuPDF Features

## Basic Operations
- **Merge PDFs** - Combine multiple PDF files into one
- **Split PDFs** - Split PDF by page ranges
- **Extract Pages** - Extract specific pages from PDF
- **Compress PDF** - Reduce PDF file size with quality levels
- **Add Watermark** - Add text watermark with opacity control
- **Encrypt PDF** - Add/remove password protection (AES-256)

## Content Extraction
- **Extract Text** - Extract text content with layout preservation
- **Extract Images** - Extract embedded images from PDF

## Conversion
- **PDF to DOCX** - Convert to Word with page range and table options
- **PDF to XLSX** - Extract tables to Excel spreadsheet
- **PDF to Images** - Convert pages to PNG/JPG images

## Encryption Features
- **Add Password**: Protect PDF with user password (AES-256 encryption)
- **Owner Password**: Optional separate password for full permissions
- **Remove Password**: Decrypt password-protected PDFs
- **Password Validation**: Verify password before decryption

## Technical Details
- All features use pure Python dependencies (no external binaries required)
- Encryption uses AES-256 algorithm via pypdf
- User password: Required to open the PDF
- Owner password: Optional, grants full permissions
- Wrong password handling with clear error messages

## Dependencies
All dependencies are Python packages with permissive licenses:
- pypdf (BSD) - PDF manipulation and encryption
- pdfplumber (MIT) - Text and table extraction
- pikepdf (MPL-2.0) - PDF compression
- python-docx (MIT) - DOCX generation
- openpyxl (MIT) - Excel generation
- Pillow (HPND) - Image processing
- reportlab (BSD-like) - Watermark generation
- PySide6 (LGPL-3.0) - GUI framework
