import pytest
import os
from pathlib import Path
from pypdf import PdfReader
from src.modules.split import Splitter


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_split_by_pages_single_page(tmp_path, test_data_dir):
    """Test splitting PDF into single-page files."""
    with Splitter(str(test_data_dir / "sample.pdf")) as splitter:
        file_count = splitter.split_by_pages(str(tmp_path), pages_per_file=1)
    
    assert file_count > 0
    assert os.path.exists(f"{tmp_path}/split_1.pdf")


def test_split_by_pages_multiple_pages(tmp_path, test_data_dir):
    """Test splitting PDF with multiple pages per file."""
    with Splitter(str(test_data_dir / "big_text.pdf")) as splitter:
        file_count = splitter.split_by_pages(str(tmp_path), pages_per_file=2)
    
    assert file_count > 0
    assert os.path.exists(f"{tmp_path}/split_1.pdf")


def test_split_multipage_pdf(tmp_path, test_data_dir):
    """Test splitting multi-page PDF."""
    with Splitter(str(test_data_dir / "big_text.pdf")) as splitter:
        file_count = splitter.split_by_pages(str(tmp_path), pages_per_file=1)
    
    assert file_count > 0
    for i in range(1, file_count + 1):
        assert os.path.exists(f"{tmp_path}/split_{i}.pdf")


def test_extract_pages(tmp_path, test_data_dir):
    """Test extracting specific pages."""
    output_path = f"{tmp_path}/extracted.pdf"
    with Splitter(str(test_data_dir / "sample.pdf")) as splitter:
        splitter.extract_pages(output_path, [0])
    
    assert os.path.exists(output_path)
    
    reader = PdfReader(output_path)
    assert len(reader.pages) == 1


def test_extract_multiple_pages(tmp_path, test_data_dir):
    """Test extracting multiple pages."""
    output_path = f"{tmp_path}/extracted.pdf"
    with Splitter(str(test_data_dir / "big_text.pdf")) as splitter:
        splitter.extract_pages(output_path, [0, 1])
    
    assert os.path.exists(output_path)
    
    reader = PdfReader(output_path)
    assert len(reader.pages) == 2


def test_extract_invalid_page(tmp_path, test_data_dir):
    """Test extracting invalid page number."""
    output_path = f"{tmp_path}/extracted.pdf"
    with Splitter(str(test_data_dir / "sample.pdf")) as splitter:
        splitter.extract_pages(output_path, [999])
    
    assert os.path.exists(output_path)
    
    reader = PdfReader(output_path)
    assert len(reader.pages) == 0


def test_split_landscape_pdf(tmp_path, test_data_dir):
    """Test splitting landscape PDF."""
    with Splitter(str(test_data_dir / "landscape.pdf")) as splitter:
        file_count = splitter.split_by_pages(str(tmp_path), pages_per_file=1)
    
    assert file_count > 0
    assert os.path.exists(f"{tmp_path}/split_1.pdf")
