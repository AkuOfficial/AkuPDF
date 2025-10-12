import pikepdf
import os


class Compressor:
    """Compress PDF files to reduce file size using pikepdf."""

    def __init__(self, input_path: str):
        self.input_path = input_path

    def compress(self, output_path: str, level: str = "medium", progress_callback=None) -> dict:
        """Compress PDF and return compression stats.
        
        Args:
            output_path: Path to save compressed PDF
            level: Compression level - "low", "medium", or "high"
            progress_callback: Optional callback for progress updates
        """
        from PIL import Image
        import io
        
        original_size = os.path.getsize(self.input_path)
        
        quality_map = {"low": 85, "medium": 60, "high": 40}
        jpeg_quality = quality_map.get(level, 60)
        
        scale_map = {"low": 1.0, "medium": 0.75, "high": 0.5}
        scale_factor = scale_map.get(level, 0.75)
        
        with pikepdf.open(self.input_path) as pdf:
            total_pages = len(pdf.pages)
            
            for idx, page in enumerate(pdf.pages):
                if progress_callback:
                    progress_callback(idx, total_pages)
                
                if "/Resources" in page and "/XObject" in page["/Resources"]:
                    for key in list(page["/Resources"]["/XObject"].keys()):
                        obj = page["/Resources"]["/XObject"][key]
                        
                        if "/Subtype" in obj and obj["/Subtype"] == "/Image":
                            try:
                                raw_image = pikepdf.PdfImage(obj)
                                pil_image = raw_image.as_pil_image()
                                
                                if scale_factor < 1.0:
                                    new_width = int(pil_image.width * scale_factor)
                                    new_height = int(pil_image.height * scale_factor)
                                    pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                                
                                img_bytes = io.BytesIO()
                                pil_image.save(img_bytes, format='JPEG', quality=jpeg_quality, optimize=True)
                                img_bytes.seek(0)
                                
                                new_image = pikepdf.Stream(pdf, img_bytes.read())
                                new_image.stream_dict = pikepdf.Dictionary(
                                    Type=pikepdf.Name("/XObject"),
                                    Subtype=pikepdf.Name("/Image"),
                                    Width=obj["/Width"],
                                    Height=obj["/Height"],
                                    ColorSpace=pikepdf.Name("/DeviceRGB"),
                                    BitsPerComponent=8,
                                    Filter=pikepdf.Name("/DCTDecode"),
                                )
                                
                                page["/Resources"]["/XObject"][key] = new_image
                            except Exception:
                                pass
            
            pdf.remove_unreferenced_resources()
            
            pdf.save(
                output_path,
                compress_streams=True,
                stream_decode_level=pikepdf.StreamDecodeLevel.generalized,
                object_stream_mode=pikepdf.ObjectStreamMode.generate,
                normalize_content=True,
                linearize=False,
            )
        
        compressed_size = os.path.getsize(output_path)
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        return {
            "original_size": original_size,
            "compressed_size": compressed_size,
            "reduction_percent": reduction
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def get_compression_levels():
        """Get available compression levels."""
        return ["low", "medium", "high"]
