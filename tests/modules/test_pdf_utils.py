import pytest
from pathlib import Path
from src.modules.pdf_utils import parse_page_numbers, get_pdf_info


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_parse_page_numbers_simple():
    """Test parsing simple page numbers."""
    result = parse_page_numbers("1,2,3")
    assert result == [0, 1, 2]


def test_parse_page_numbers_range():
    """Test parsing page ranges."""
    result = parse_page_numbers("1-3")
    assert result == [0, 1, 2]


def test_parse_page_numbers_mixed():
    """Test parsing mixed page numbers and ranges."""
    result = parse_page_numbers("1,3-5,7")
    assert result == [0, 2, 3, 4, 6]


def test_parse_page_numbers_extra_spaces():
    """Test parsing with extra spaces."""
    result = parse_page_numbers("  1 , 3 - 5 , 7  ")
    assert result == [0, 2, 3, 4, 6]


def test_parse_page_numbers_extra_commas():
    """Test parsing with extra commas."""
    result = parse_page_numbers("1,,3,,,5")
    assert result == [0, 2, 4]


def test_parse_page_numbers_trailing_commas():
    """Test parsing with trailing commas."""
    result = parse_page_numbers(",1,3,5,")
    assert result == [0, 2, 4]


def test_parse_page_numbers_invalid_format():
    """Test parsing invalid format."""
    assert parse_page_numbers("abc") is None
    assert parse_page_numbers("1-2-3") is None
    assert parse_page_numbers("5-3") is None
    assert parse_page_numbers("0") is None
    assert parse_page_numbers("-1") is None


def test_parse_page_numbers_empty():
    """Test parsing empty input."""
    assert parse_page_numbers("") is None
    assert parse_page_numbers("   ") is None
    assert parse_page_numbers(",,,") is None


def test_get_pdf_info_valid_file(test_data_dir):
    """Test getting PDF info from valid file."""
    pdf_path = str(test_data_dir / "sample.pdf")
    info = get_pdf_info(pdf_path)
    
    assert 'total_pages' in info
    assert info['total_pages'] > 0


def test_get_pdf_info_multipage(test_data_dir):
    """Test getting PDF info from multi-page file."""
    pdf_path = str(test_data_dir / "big_text.pdf")
    info = get_pdf_info(pdf_path)
    
    assert info['total_pages'] >= 1


def test_get_pdf_info_invalid_file():
    """Test getting PDF info from non-existent file."""
    with pytest.raises(Exception):
        get_pdf_info("nonexistent.pdf")
