from pypdf import PdfReader, PdfWriter


class Splitter:
    """Split PDF files into separate documents."""

    def __init__(self, input_path: str):
        self.input_path = input_path
        self.reader = PdfReader(input_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reader = None

    def split_by_pages(self, output_dir: str, pages_per_file: int = 1):
        """Split PDF into multiple files with specified pages per file."""
        total_pages = len(self.reader.pages)
        
        file_count = 0
        for start_page in range(0, total_pages, pages_per_file):
            writer = PdfWriter()
            end_page = min(start_page + pages_per_file, total_pages)
            
            for page_num in range(start_page, end_page):
                writer.add_page(self.reader.pages[page_num])
            
            output_path = f"{output_dir}/split_{file_count + 1}.pdf"
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            file_count += 1
        
        return file_count

    def extract_pages(self, output_path: str, page_numbers: list[int]):
        """Extract specific pages from PDF."""
        writer = PdfWriter()
        
        for page_num in page_numbers:
            if 0 <= page_num < len(self.reader.pages):
                writer.add_page(self.reader.pages[page_num])
        
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
