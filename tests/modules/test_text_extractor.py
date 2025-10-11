import pytest
from pathlib import Path
from src.modules.text_extractor import TextExtractor


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_text_extractor_context_manager(test_data_dir):
    """Test TextExtractor can be used as context manager."""
    pdf_path = str(test_data_dir / "sample.pdf")
    with TextExtractor(pdf_path) as extractor:
        assert extractor is not None


def test_extract_all_text(test_data_dir):
    """Test extracting all text from PDF."""
    pdf_path = str(test_data_dir / "sample.pdf")
    with TextExtractor(pdf_path) as extractor:
        text = extractor.extract_all_text()
        assert isinstance(text, str)
        assert len(text) > 0


def test_extract_all_text_with_layout(test_data_dir):
    """Test extracting text with layout preservation."""
    pdf_path = str(test_data_dir / "sample.pdf")
    with TextExtractor(pdf_path) as extractor:
        text = extractor.extract_all_text(preserve_layout=True)
        assert isinstance(text, str)
        assert len(text) > 0


def test_extract_page_text(test_data_dir):
    """Test extracting text from specific pages."""
    pdf_path = str(test_data_dir / "sample.pdf")
    with TextExtractor(pdf_path) as extractor:
        text = extractor.extract_page_text([0])
        assert isinstance(text, str)
        assert "Page 1" in text


def test_extract_page_text_with_layout(test_data_dir):
    """Test extracting text from specific pages with layout."""
    pdf_path = str(test_data_dir / "sample.pdf")
    with TextExtractor(pdf_path) as extractor:
        text = extractor.extract_page_text([0], preserve_layout=True)
        assert isinstance(text, str)
        assert "Page 1" in text


def test_extract_invalid_page(test_data_dir):
    """Test extracting from invalid page numbers."""
    pdf_path = str(test_data_dir / "sample.pdf")
    with TextExtractor(pdf_path) as extractor:
        text = extractor.extract_page_text([999])
        assert text == ""


def test_extract_empty_page_list(test_data_dir):
    """Test extracting with empty page list."""
    pdf_path = str(test_data_dir / "sample.pdf")
    with TextExtractor(pdf_path) as extractor:
        text = extractor.extract_page_text([])
        assert text == ""
