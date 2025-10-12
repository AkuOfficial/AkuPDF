import pytest
from pathlib import Path
from src.ui.image_extract_view import ImageExtractView


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_image_extract_view_initialization(qtbot):
    """Test that ImageExtractView initializes correctly."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    
    assert view.input_file is None
    assert view.total_pages == 0
    assert not view.options_section.isEnabled()
    assert not view.actions_section.isEnabled()


def test_load_file(qtbot, test_data_dir):
    """Test loading a PDF file."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view._load_file(str(test_data_dir / "images.pdf"))
    
    assert view.input_file is not None
    assert view.total_pages > 0
    assert not view.drop_zone.isVisible()
    assert view.file_info_container.isVisible()
    assert view.options_section.isEnabled()
    assert view.actions_section.isEnabled()


def test_clear_file(qtbot, test_data_dir):
    """Test clearing the selected file."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view._load_file(str(test_data_dir / "images.pdf"))
    view.clear_file()
    
    assert view.input_file is None
    assert view.total_pages == 0
    assert view.drop_zone.isVisible()
    assert not view.file_info_container.isVisible()
    assert not view.options_section.isEnabled()
    assert not view.actions_section.isEnabled()


def test_status_message(qtbot):
    """Test showing and hiding status messages."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    view.show()
    
    assert not view.status_container.isVisible()
    
    view._show_status("Test message", "info")
    assert view.status_container.isVisible()
    
    view._hide_status()
    assert not view.status_container.isVisible()


def test_extract_without_file(qtbot):
    """Test extracting without selecting a file."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view.extract_images()
    assert view.status_container.isVisible()
    assert "select a pdf file" in view.status_label.text().lower()


def test_page_selection_radio_buttons(qtbot):
    """Test page selection radio buttons exist and work."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    
    assert view.all_pages_radio is not None
    assert view.specific_pages_radio is not None
    assert view.all_pages_radio.isChecked()
    assert not view.specific_pages_radio.isChecked()


def test_pages_input_disabled_by_default(qtbot):
    """Test pages input is disabled when all pages is selected."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    
    assert not view.pages_input.isEnabled()


def test_pages_input_enabled_when_specific_selected(qtbot, test_data_dir):
    """Test pages input is enabled when specific pages is selected."""
    view = ImageExtractView()
    qtbot.addWidget(view)
    view.show()
    
    view._load_file(str(test_data_dir / "images.pdf"))
    view.specific_pages_radio.setChecked(True)
    assert view.pages_input.isEnabled()
