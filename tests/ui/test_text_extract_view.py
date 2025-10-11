import pytest
from pathlib import Path
from src.ui.text_extract_view import TextExtractView


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_text_extract_view_initialization(qtbot):
    """Test that TextExtractView initializes correctly."""
    view = TextExtractView()
    qtbot.addWidget(view)
    
    assert view.input_file is None
    assert view.total_pages == 0
    assert not view.options_section.isEnabled()
    assert not view.actions_section.isEnabled()
    assert not view.result_section.isVisible()


def test_load_file(qtbot, test_data_dir):
    """Test loading a PDF file."""
    view = TextExtractView()
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
    view = TextExtractView()
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
    assert not view.result_section.isVisible()


def test_status_message(qtbot):
    """Test showing and hiding status messages."""
    view = TextExtractView()
    qtbot.addWidget(view)
    view.show()
    
    assert not view.status_container.isVisible()
    
    view._show_status("Test message", "info")
    assert view.status_container.isVisible()
    
    view._hide_status()
    assert not view.status_container.isVisible()


def test_extract_without_file(qtbot):
    """Test extracting without selecting a file."""
    view = TextExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view.extract_text()
    assert view.status_container.isVisible()
    assert "select a pdf file" in view.status_label.text().lower()


def test_layout_checkbox_exists(qtbot):
    """Test that layout preservation checkbox exists."""
    view = TextExtractView()
    qtbot.addWidget(view)
    
    assert view.layout_checkbox is not None
    assert not view.layout_checkbox.isChecked()


def test_text_display_exists(qtbot):
    """Test that text display widget exists."""
    view = TextExtractView()
    qtbot.addWidget(view)
    
    assert view.text_display is not None
    assert view.text_display.isReadOnly()


def test_save_button_disabled_initially(qtbot):
    """Test that save button is disabled initially."""
    view = TextExtractView()
    qtbot.addWidget(view)
    
    assert not view.save_btn.isEnabled()
