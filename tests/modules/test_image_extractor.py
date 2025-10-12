import pytest
from pathlib import Path
import os
import tempfile
from src.modules.image_extractor import ImageExtractor


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_image_extractor_context_manager(test_data_dir):
    """Test ImageExtractor can be used as context manager."""
    pdf_path = str(test_data_dir / "images.pdf")
    with ImageExtractor(pdf_path) as extractor:
        assert extractor is not None


def test_extract_all_images(test_data_dir, temp_output_dir):
    """Test extracting all images from PDF."""
    pdf_path = str(test_data_dir / "images.pdf")
    with ImageExtractor(pdf_path) as extractor:
        count = extractor.extract_all_images(temp_output_dir)
        assert count > 0
        assert len(os.listdir(temp_output_dir)) == count


def test_extract_specific_page_images(test_data_dir, temp_output_dir):
    """Test extracting images from specific pages."""
    pdf_path = str(test_data_dir / "images.pdf")
    with ImageExtractor(pdf_path) as extractor:
        count = extractor.extract_page_images(temp_output_dir, [0])
        assert count >= 0
        assert len(os.listdir(temp_output_dir)) == count


def test_extract_multiple_pages_images(test_data_dir, temp_output_dir):
    """Test extracting images from multiple pages."""
    pdf_path = str(test_data_dir / "images.pdf")
    with ImageExtractor(pdf_path) as extractor:
        count = extractor.extract_page_images(temp_output_dir, [0, 1, 2])
        assert count > 0


def test_extract_invalid_page(test_data_dir, temp_output_dir):
    """Test extracting from invalid page numbers."""
    pdf_path = str(test_data_dir / "images.pdf")
    with ImageExtractor(pdf_path) as extractor:
        count = extractor.extract_page_images(temp_output_dir, [999])
        assert count == 0


def test_extract_empty_page_list(test_data_dir, temp_output_dir):
    """Test extracting with empty page list."""
    pdf_path = str(test_data_dir / "images.pdf")
    with ImageExtractor(pdf_path) as extractor:
        count = extractor.extract_page_images(temp_output_dir, [])
        assert count == 0


def test_extracted_files_exist(test_data_dir, temp_output_dir):
    """Test that extracted files are created."""
    pdf_path = str(test_data_dir / "images.pdf")
    with ImageExtractor(pdf_path) as extractor:
        count = extractor.extract_all_images(temp_output_dir)
        files = os.listdir(temp_output_dir)
        assert len(files) == count
        for file in files:
            assert os.path.getsize(os.path.join(temp_output_dir, file)) > 0


def test_extract_mixed_content(test_data_dir, temp_output_dir):
    """Test extracting images from PDF with mixed content."""
    pdf_path = str(test_data_dir / "mixed_content.pdf")
    with ImageExtractor(pdf_path) as extractor:
        count = extractor.extract_all_images(temp_output_dir)
        assert count == 3
        files = os.listdir(temp_output_dir)
        assert len(files) == 3
