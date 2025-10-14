from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


class Watermarker:
    """Add watermarks to PDF files."""

    def __init__(self, input_path: str):
        self.input_path = input_path

    def add_watermark(self, output_path: str, text: str, opacity: float = 0.3) -> dict:
        """Add text watermark to PDF.
        
        Args:
            output_path: Path to save watermarked PDF
            text: Watermark text
            opacity: Watermark opacity (0.0 to 1.0)
        
        Returns:
            dict with watermark stats
        """
        import os
        
        reader = PdfReader(self.input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            font_size = min(60, page_width / len(text) * 1.5)
            
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            can.setFillAlpha(opacity)
            can.setFont("Helvetica-Bold", font_size)
            can.saveState()
            can.translate(page_width / 2, page_height / 2)
            can.rotate(45)
            can.drawCentredString(0, 0, text)
            can.restoreState()
            can.save()
            
            packet.seek(0)
            watermark = PdfReader(packet)
            page.merge_page(watermark.pages[0])
            writer.add_page(page)
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return {
            "input_file": self.input_path,
            "output_file": output_path,
            "output_size": os.path.getsize(output_path),
            "page_count": len(reader.pages)
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
