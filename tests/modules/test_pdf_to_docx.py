import pytest
import os
from pathlib import Path
from src.modules.pdf_to_docx import PdfToDocxConverter


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_convert_basic(tmp_path, test_data_dir):
    """Test basic PDF to DOCX conversion."""
    output_path = tmp_path / "output.docx"
    with PdfToDocxConverter(str(test_data_dir / "sample.pdf")) as converter:
        result = converter.convert(str(output_path))
    
    assert os.path.exists(output_path)
    assert result["output_size"] > 0


def test_convert_multipage(tmp_path, test_data_dir):
    """Test converting multipage PDF."""
    output_path = tmp_path / "output.docx"
    with PdfToDocxConverter(str(test_data_dir / "multipage_text.pdf")) as converter:
        result = converter.convert(str(output_path))
    
    assert os.path.exists(output_path)
    assert result["output_file"] == str(output_path)


def test_convert_with_images(tmp_path, test_data_dir):
    """Test converting PDF with images."""
    output_path = tmp_path / "output.docx"
    with PdfToDocxConverter(str(test_data_dir / "mixed_content.pdf")) as converter:
        result = converter.convert(str(output_path))
    
    assert os.path.exists(output_path)
    assert result["output_size"] > 0
