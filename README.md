# 📘 AkuPDF

## 📝 Description
**AkuPDF** is a comprehensive desktop application suite for PDF processing and manipulation. 
Built with Python and PySide6, it provides a modern, 
futuristic interface for all your PDF needs - from basic operations like merging and splitting 
to advanced features like encryption, content extraction, and format conversion.

## ⚖️ License Notice
> 🛑 **This repository is for demonstration and portfolio purposes only.**  
> Redistribution, modification, or resale of this code is **strictly prohibited** without explicit permission from the author.

## 🚀 Features

### 📄 Basic Operations
- **Merge PDFs** - Combine multiple PDF files into a single document
- **Split PDFs** - Separate PDFs by page ranges or individual pages
- **Extract Pages** - Extract specific pages from PDF files
- **Compress PDF** - Reduce file size with adjustable quality levels
- **Add Watermark** - Apply text watermarks with opacity control

### 🔐 Security & Encryption
- **Add Password Protection** - Secure PDFs with AES-256 encryption
  - User password for viewing access
  - Owner password for editing permissions
- **Remove Password Protection** - Decrypt protected PDFs
  - Password-based decryption
  - Recovery mode for weakly protected files

### 📝 Content Extraction
- **Extract Text** - Extract text content with layout preservation options
- **Extract Images** - Extract all embedded images from PDF pages

### 🔄 Format Conversion
- **PDF to DOCX** - Convert to Microsoft Word with table extraction
- **PDF to XLSX** - Extract tables to Excel spreadsheets
- **PDF to Images** - Convert pages to PNG/JPG images

### 🎨 User Interface
- **Modern Design** - Futuristic interface with gradient backgrounds
- **Organized Navigation** - Categorized sidebar with grouped features
- **Drag & Drop Support** - Intuitive file handling
- **Real-time Progress** - Visual feedback for all operations

## 🛠️ Technical Stack
- **GUI Framework**: PySide6 (Qt6) with custom styling
- **PDF Processing**: pypdf, pikepdf, pdfplumber
- **Document Generation**: python-docx, openpyxl, reportlab
- **Image Processing**: Pillow
- **Security**: AES-256 encryption via pypdf
- **Build System**: Poetry for dependency management

## 🏗️ Architecture
- **Modular Design** - Separate modules for each PDF operation
- **Clean UI Separation** - Distinct view classes for each feature
- **Pure Python** - No external binaries required
- **Cross-platform** - Works on Windows, macOS, and Linux

## 📁 Project Structure
```
AkuPDF/
├── src/
│   ├── modules/          # Core PDF processing logic
│   ├── ui/              # User interface components
│   └── app.py           # Main application entry
├── tests/               # Comprehensive test suite
├── docs/                # Documentation
└── licenses/            # Third-party licenses
```