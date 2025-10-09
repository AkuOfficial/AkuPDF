import pytest
from PySide6.QtWidgets import QApplication
from src.ui.split_view import SplitView


@pytest.fixture(scope="module")
def app():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def split_view(app):
    """Create SplitView instance for tests."""
    view = SplitView()
    view.show()
    yield view


def test_split_view_creation(split_view):
    """Test that split view is created successfully."""
    assert split_view is not None


def test_split_view_initial_state(split_view):
    """Test that split view starts with no file selected."""
    assert split_view.input_file is None
    assert split_view.total_pages == 0
    assert "No file selected" in split_view.file_label.text()


def test_split_view_has_spinbox(split_view):
    """Test that split view has pages spinbox."""
    assert split_view.pages_spinbox is not None
    assert split_view.pages_spinbox.value() == 1
    assert split_view.pages_spinbox.minimum() == 1


def test_split_view_has_slider(split_view):
    """Test that split view has pages slider."""
    assert split_view.pages_slider is not None
    assert split_view.pages_slider.value() == 1
    assert split_view.pages_slider.minimum() == 1


def test_split_view_has_page_range_label(split_view):
    """Test that split view has page range label."""
    assert split_view.page_range_label is not None
    assert split_view.page_range_label.text() == "(Max: 1)"


def test_split_view_has_status_container(split_view):
    """Test that status container exists."""
    assert split_view.status_container is not None
    assert not split_view.status_container.isVisible()


def test_split_view_options_disabled_initially(split_view):
    """Test that options are disabled until file is selected."""
    assert not split_view.options_section.isEnabled()
    assert not split_view.actions_section.isEnabled()


def test_drop_zone_visible_initially(split_view):
    """Test that drop zone is visible initially."""
    assert split_view.drop_zone.isVisible()
    assert not split_view.file_info_container.isVisible()


def test_clear_file(split_view):
    """Test clearing selected file."""
    split_view.input_file = "test.pdf"
    split_view.total_pages = 10
    split_view.file_label.setText("test.pdf")
    split_view.page_info_label.setText("Total pages: 10")
    split_view.options_section.setEnabled(True)
    split_view.actions_section.setEnabled(True)
    
    split_view.clear_file()
    
    assert split_view.input_file is None
    assert split_view.total_pages == 0
    assert "No file selected" in split_view.file_label.text()
    assert split_view.page_info_label.text() == ""
    assert not split_view.options_section.isEnabled()
    assert not split_view.actions_section.isEnabled()


def test_spinbox_maximum_reset_on_clear(split_view):
    """Test that spinbox maximum is reset when clearing file."""
    split_view.pages_spinbox.setMaximum(50)
    split_view.pages_spinbox.setValue(10)
    
    split_view.clear_file()
    
    assert split_view.pages_spinbox.maximum() == 1
    assert split_view.pages_spinbox.value() == 1


def test_slider_maximum_reset_on_clear(split_view):
    """Test that slider maximum is reset when clearing file."""
    split_view.pages_slider.setMaximum(50)
    split_view.pages_slider.setValue(10)
    split_view.page_range_label.setText("(Max: 50)")
    
    split_view.clear_file()
    
    assert split_view.pages_slider.maximum() == 1
    assert split_view.pages_slider.value() == 1
    assert split_view.page_range_label.text() == "(Max: 1)"


def test_spinbox_slider_sync_from_spinbox(split_view):
    """Test that slider syncs when spinbox changes."""
    split_view.pages_spinbox.setMaximum(10)
    split_view.pages_slider.setMaximum(10)
    
    split_view._sync_slider_from_spinbox(5)
    assert split_view.pages_slider.value() == 5


def test_spinbox_slider_sync_from_slider(split_view):
    """Test that spinbox syncs when slider changes."""
    split_view.pages_spinbox.setMaximum(10)
    split_view.pages_slider.setMaximum(10)
    
    split_view._sync_spinbox_from_slider(7)
    assert split_view.pages_spinbox.value() == 7


def test_show_status_success(split_view):
    """Test showing success status message."""
    split_view._show_status("Test success message", "success")
    
    assert split_view.status_container.isVisible()
    assert "Test success message" in split_view.status_label.text()


def test_show_status_error(split_view):
    """Test showing error status message."""
    split_view._show_status("Test error message", "error")
    
    assert split_view.status_container.isVisible()
    assert "Test error message" in split_view.status_label.text()


def test_hide_status(split_view):
    """Test hiding status message."""
    split_view._show_status("Test message", "info")
    assert split_view.status_container.isVisible()
    
    split_view._hide_status()
    assert not split_view.status_container.isVisible()


def test_back_callback(app):
    """Test that back callback is set."""
    callback_called = []
    
    def on_back_click():
        callback_called.append(True)
    
    view = SplitView(on_back_click=on_back_click)
    assert view is not None
