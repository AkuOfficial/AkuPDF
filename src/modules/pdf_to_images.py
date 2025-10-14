import pdfplumber
import os


class PdfToImagesConverter:
    """Convert PDF pages to images."""

    def __init__(self, input_path: str):
        self.input_path = input_path

    def convert(self, output_folder: str, image_format: str = "png", dpi: int = 150) -> dict:
        """Convert PDF pages to images.
        
        Args:
            output_folder: Folder to save images
            image_format: Image format (png, jpg, jpeg)
            dpi: Resolution in DPI
        
        Returns:
            dict with conversion stats
        """
        os.makedirs(output_folder, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        
        image_paths = []
        total_size = 0
        
        with pdfplumber.open(self.input_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                img = page.to_image(resolution=dpi)
                image_path = os.path.join(output_folder, f"{base_name}_page_{page_num + 1}.{image_format}")
                img.save(image_path)
                
                image_paths.append(image_path)
                total_size += os.path.getsize(image_path)
        
        return {
            "input_file": self.input_path,
            "output_folder": output_folder,
            "page_count": len(image_paths),
            "total_size": total_size,
            "image_paths": image_paths
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
