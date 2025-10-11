import pdfplumber


class TextExtractor:
    """Extract text from PDF files using pdfplumber."""

    def __init__(self, input_path: str):
        self.input_path = input_path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def extract_all_text(self, preserve_layout: bool = False):
        """Extract text from all pages.
        
        Args:
            preserve_layout: If True, attempts to preserve text layout/positioning
            
        Returns:
            str: Extracted text from all pages
        """
        text_parts = []
        with pdfplumber.open(self.input_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                if preserve_layout:
                    text = page.extract_text(layout=True)
                else:
                    text = page.extract_text()
                
                if text:
                    text_parts.append(f"--- Page {page_num} ---\n{text}")
        
        return "\n\n".join(text_parts) if text_parts else ""

    def extract_page_text(self, page_numbers: list[int], preserve_layout: bool = False):
        """Extract text from specific pages.
        
        Args:
            page_numbers: List of page indices (0-based)
            preserve_layout: If True, attempts to preserve text layout/positioning
            
        Returns:
            str: Extracted text from specified pages
        """
        text_parts = []
        with pdfplumber.open(self.input_path) as pdf:
            for page_idx in page_numbers:
                if 0 <= page_idx < len(pdf.pages):
                    page = pdf.pages[page_idx]
                    if preserve_layout:
                        text = page.extract_text(layout=True)
                    else:
                        text = page.extract_text()
                    
                    if text:
                        text_parts.append(f"--- Page {page_idx + 1} ---\n{text}")
        
        return "\n\n".join(text_parts) if text_parts else ""
