"""PDF encryption and decryption module."""
import os
from pypdf import PdfReader, PdfWriter


class PDFEncryptor:
    """Encrypt and decrypt PDF files."""

    def __init__(self, input_path):
        self.input_path = input_path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_password(self, output_path, user_password, owner_password=None):
        """Add password protection to PDF.
        
        Args:
            output_path: Path to save encrypted PDF
            user_password: Password for opening the PDF
            owner_password: Password for full permissions (optional)
            
        Returns:
            dict with output_size and page_count
        """
        reader = PdfReader(self.input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(
            user_password=user_password,
            owner_password=owner_password or user_password,
            algorithm="AES-256"
        )

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return {
            "output_size": os.path.getsize(output_path),
            "page_count": len(reader.pages)
        }

    def remove_password(self, output_path, password):
        """Remove password protection from PDF.
        
        Args:
            output_path: Path to save decrypted PDF
            password: Current password to decrypt
            
        Returns:
            dict with output_size and page_count
        """
        reader = PdfReader(self.input_path)
        
        if reader.is_encrypted:
            if not reader.decrypt(password):
                raise ValueError("Incorrect password")

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return {
            "output_size": os.path.getsize(output_path),
            "page_count": len(reader.pages)
        }
