import pdfplumber
from PIL import Image
import io
import os


class ImageExtractor:
    """Extract images from PDF files using pdfplumber."""

    def __init__(self, input_path: str):
        self.input_path = input_path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def extract_all_images(self, output_dir: str):
        """Extract all images from all pages.
        
        Returns:
            int: Number of images extracted
        """
        image_count = 0
        with pdfplumber.open(self.input_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                for img_idx, img_info in enumerate(page.images, 1):
                    self._save_image(img_info, output_dir, page_num, img_idx)
                    image_count += 1
        return image_count

    def extract_page_images(self, output_dir: str, page_numbers: list[int]):
        """Extract images from specific pages.
        
        Args:
            output_dir: Directory to save images
            page_numbers: List of page indices (0-based)
            
        Returns:
            int: Number of images extracted
        """
        image_count = 0
        with pdfplumber.open(self.input_path) as pdf:
            for page_idx in page_numbers:
                if 0 <= page_idx < len(pdf.pages):
                    page = pdf.pages[page_idx]
                    for img_idx, img_info in enumerate(page.images, 1):
                        self._save_image(img_info, output_dir, page_idx + 1, img_idx)
                        image_count += 1
        return image_count

    def _save_image(self, img_info, output_dir, page_num, img_idx):
        """Save image to file."""
        try:
            stream = img_info['stream']
            image_data = stream.get_data()
            
            # Try to open as image
            img = Image.open(io.BytesIO(image_data))
            
            # Determine format
            img_format = img.format if img.format else 'PNG'
            ext = img_format.lower()
            
            # Save image
            filename = f"page_{page_num}_image_{img_idx}.{ext}"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath)
            
        except Exception as e:
            # If PIL fails, save raw data
            filename = f"page_{page_num}_image_{img_idx}.bin"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(image_data)
