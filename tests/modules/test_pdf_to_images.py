import pytest
import os
from src.modules.pdf_to_images import PdfToImagesConverter


@pytest.fixture
def sample_pdf():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests", "data", "sample.pdf")


@pytest.fixture
def output_folder(tmp_path):
    return str(tmp_path / "images")


def test_basic_conversion_png(sample_pdf, output_folder):
    """Test basic PDF to PNG conversion."""
    with PdfToImagesConverter(sample_pdf) as converter:
        result = converter.convert(output_folder, image_format="png", dpi=150)
    
    assert os.path.exists(output_folder)
    assert result["page_count"] > 0
    assert result["total_size"] > 0
    assert len(result["image_paths"]) == result["page_count"]
    
    for image_path in result["image_paths"]:
        assert os.path.exists(image_path)
        assert image_path.endswith(".png")


def test_conversion_jpg(sample_pdf, output_folder):
    """Test PDF to JPG conversion."""
    with PdfToImagesConverter(sample_pdf) as converter:
        result = converter.convert(output_folder, image_format="jpg", dpi=150)
    
    assert os.path.exists(output_folder)
    assert result["page_count"] > 0
    
    for image_path in result["image_paths"]:
        assert os.path.exists(image_path)
        assert image_path.endswith(".jpg")


def test_high_dpi_conversion(sample_pdf, output_folder):
    """Test conversion with high DPI."""
    with PdfToImagesConverter(sample_pdf) as converter:
        result_low = converter.convert(output_folder + "_low", image_format="png", dpi=72)
        result_high = converter.convert(output_folder + "_high", image_format="png", dpi=300)
    
    assert result_high["total_size"] > result_low["total_size"]
