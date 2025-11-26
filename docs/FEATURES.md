# AkuPDF Features

## Basic Operations
- **Merge PDFs** - Combine multiple PDF files into one
- **Split PDFs** - Split PDF by page ranges
- **Extract Pages** - Extract specific pages from PDF
- **Compress PDF** - Reduce PDF file size with quality levels
- **Add Watermark** - Add text watermark with opacity control
- **Add Password** - Add password protection (AES-256)
- **Remove Password** - Remove password protection

## Content Extraction
- **Extract Text** - Extract text content with layout preservation
- **Extract Images** - Extract embedded images from PDF

## Conversion
- **PDF to DOCX** - Convert to Word with page range and table options
- **PDF to XLSX** - Extract tables to Excel spreadsheet
- **PDF to Images** - Convert pages to PNG/JPG images

## Encryption Features

### Add Password Protection
- **User Password**: Required password to open and view the PDF (AES-256 encryption)
- **Owner Password**: Optional separate password that grants full permissions (edit, print, copy)
  - If not set, the user password will be used as the owner password
  - Allows you to restrict what users can do even after opening the PDF
  - Example: Set user password for viewing, owner password for editing

### Remove Password Protection
- **With Password**: Decrypt PDF when you know the user or owner password
- **Without Password (Recovery)**: Attempt to remove encryption without knowing the password
  - Only works for PDFs with weak or no owner password protection
  - Cannot decrypt PDFs with strong user password protection
  - Success depends on the PDF's encryption settings

## Technical Details
- All features use pure Python dependencies (no external binaries required)
- Encryption uses AES-256 algorithm via pypdf
- Password recovery uses pikepdf for advanced PDF manipulation
- Clear error messages for wrong passwords or failed recovery attempts

## Dependencies
All dependencies are Python packages with permissive licenses:
- PySide6 (LGPL-3.0) - GUI framework
- pypdf (BSD-3-Clause) - PDF manipulation and encryption
- qt-material (BSD-2-Clause) - Material design styling
- pdfplumber (MIT) - Text and table extraction
- pikepdf (MPL-2.0) - Advanced PDF manipulation and compression
- python-docx (MIT) - DOCX generation
- openpyxl (MIT) - Excel generation
- Pillow (MIT) - Image processing
- reportlab (BSD-3-Clause) - Watermark generation
