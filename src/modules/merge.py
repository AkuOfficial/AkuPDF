import os
from pypdf import PdfWriter, PdfReader


class Merger:
    def __init__(self):
        self.engine = PdfWriter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.engine.close()

    def process(self, input_files: list[str], output_file: str = "merged.pdf"):
        if not input_files:
            raise ValueError("No input files provided for merging")

        if os.path.exists(output_file):
            raise FileExistsError(f"Output file already exists: {output_file}")

        for pdf in input_files:
            if not pdf.lower().endswith('.pdf'):
                raise ValueError(f"Invalid file type: {pdf}. Only PDF files are supported.")
            
            if not os.path.exists(pdf):
                raise FileNotFoundError(f"File not found: {pdf}")
            
            try:
                # Try to read and append with non-strict mode for better compatibility
                reader = PdfReader(pdf, strict=False)
                for page in reader.pages:
                    self.engine.add_page(page)
            except Exception as e:
                raise ValueError(f"Cannot process PDF file: {pdf}. Error: {str(e)}")

        self.engine.write(output_file)
