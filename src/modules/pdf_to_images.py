from pypdf import PdfReader
from PIL import Image
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
        
        reader = PdfReader(self.input_path)
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        
        scale = dpi / 72.0
        
        image_paths = []
        total_size = 0
        
        for page_num, page in enumerate(reader.pages):
            if "/XObject" in page['/Resources']:
                x_object = page['/Resources']['/XObject'].get_object()
                
                for obj_name in x_object:
                    obj = x_object[obj_name]
                    
                    if obj['/Subtype'] == '/Image':
                        size = (int(obj['/Width'] * scale), int(obj['/Height'] * scale))
                        data = obj.get_data()
                        
                        if obj['/ColorSpace'] == '/DeviceRGB':
                            mode = "RGB"
                        else:
                            mode = "P"
                        
                        img = Image.frombytes(mode, (obj['/Width'], obj['/Height']), data)
                        img = img.resize(size, Image.Resampling.LANCZOS)
                        
                        image_path = os.path.join(output_folder, f"{base_name}_page_{page_num + 1}.{image_format}")
                        img.save(image_path)
                        
                        image_paths.append(image_path)
                        total_size += os.path.getsize(image_path)
                        break
        
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
