import pytest
from pathlib import Path
from src.ui.extract_view import ExtractView


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_extract_view_initialization(qtbot):
    """Test that ExtractView initializes correctly."""
    view = ExtractView()
    qtbot.addWidget(view)
    
    assert view.input_file is None
    assert view.total_pages == 0
    assert not view.options_section.isEnabled()
    assert not view.actions_section.isEnabled()


def test_parse_page_numbers_simple():
    """Test parsing simple page numbers."""
    result = ExtractView._parse_page_numbers("1,2,3")
    assert result == [0, 1, 2]


def test_parse_page_numbers_range():
    """Test parsing page ranges."""
    result = ExtractView._parse_page_numbers("1-3")
    assert result == [0, 1, 2]


def test_parse_page_numbers_mixed():
    """Test parsing mixed page numbers and ranges."""
    result = ExtractView._parse_page_numbers("1,3-5,7")
    assert result == [0, 2, 3, 4, 6]


def test_parse_page_numbers_extra_spaces():
    """Test parsing with extra spaces."""
    result = ExtractView._parse_page_numbers("  1 , 3 - 5 , 7  ")
    assert result == [0, 2, 3, 4, 6]


def test_parse_page_numbers_extra_commas():
    """Test parsing with extra commas."""
    result = ExtractView._parse_page_numbers("1,,3,,,5")
    assert result == [0, 2, 4]


def test_parse_page_numbers_trailing_commas():
    """Test parsing with trailing commas."""
    result = ExtractView._parse_page_numbers(",1,3,5,")
    assert result == [0, 2, 4]


def test_parse_page_numbers_invalid_format():
    """Test parsing invalid format."""
    assert ExtractView._parse_page_numbers("abc") is None
    assert ExtractView._parse_page_numbers("1-2-3") is None
    assert ExtractView._parse_page_numbers("5-3") is None
    assert ExtractView._parse_page_numbers("0") is None
    assert ExtractView._parse_page_numbers("-1") is None


def test_parse_page_numbers_empty():
    """Test parsing empty input."""
    assert ExtractView._parse_page_numbers("") is None
    assert ExtractView._parse_page_numbers("   ") is None
    assert ExtractView._parse_page_numbers(",,,") is None


def test_load_file(qtbot, test_data_dir):
    """Test loading a PDF file."""
    view = ExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view._load_file(str(test_data_dir / "sample.pdf"))
    
    assert view.input_file is not None
    assert view.total_pages > 0
    assert not view.drop_zone.isVisible()
    assert view.file_info_container.isVisible()
    assert view.options_section.isEnabled()
    assert view.actions_section.isEnabled()


def test_clear_file(qtbot, test_data_dir):
    """Test clearing the selected file."""
    view = ExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view._load_file(str(test_data_dir / "sample.pdf"))
    view.clear_file()
    
    assert view.input_file is None
    assert view.total_pages == 0
    assert view.drop_zone.isVisible()
    assert not view.file_info_container.isVisible()
    assert not view.options_section.isEnabled()
    assert not view.actions_section.isEnabled()


def test_status_message(qtbot):
    """Test showing and hiding status messages."""
    view = ExtractView()
    qtbot.addWidget(view)
    view.show()
    
    assert not view.status_container.isVisible()
    
    view._show_status("Test message", "info")
    assert view.status_container.isVisible()
    
    view._hide_status()
    assert not view.status_container.isVisible()


def test_extract_without_file(qtbot):
    """Test extracting without selecting a file."""
    view = ExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view.extract_pages()
    assert view.status_container.isVisible()
    assert "select a pdf file" in view.status_label.text().lower()


def test_extract_without_page_numbers(qtbot, test_data_dir):
    """Test extracting without entering page numbers."""
    view = ExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view._load_file(str(test_data_dir / "sample.pdf"))
    view.extract_pages()
    
    assert view.status_container.isVisible()
    assert "enter page numbers" in view.status_label.text().lower()
