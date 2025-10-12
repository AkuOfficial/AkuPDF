import pytest
from PySide6.QtWidgets import QApplication
from src.ui.compress_view import CompressView


@pytest.fixture(scope="module")
def app():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def compress_view(app):
    """Create CompressView instance for tests."""
    view = CompressView()
    view.show()
    yield view


def test_compress_view_creation(compress_view):
    """Test that compress view is created successfully."""
    assert compress_view is not None


def test_compress_view_has_drop_zone(compress_view):
    """Test that drop zone exists."""
    assert compress_view.drop_zone is not None


def test_compress_view_has_buttons(compress_view):
    """Test that all buttons exist."""
    assert compress_view.compress_btn is not None
    assert compress_view.clear_btn is not None


def test_buttons_disabled_initially(compress_view):
    """Test that buttons are disabled initially."""
    assert not compress_view.compress_btn.isEnabled()
    assert not compress_view.clear_btn.isEnabled()


def test_compress_view_initial_state(compress_view):
    """Test that compress view starts with no file."""
    assert compress_view.current_file is None
    assert not compress_view.file_info.isVisible()


def test_file_selection_enables_buttons(compress_view):
    """Test that selecting a file enables buttons."""
    compress_view._on_file_selected("test.pdf")
    
    assert compress_view.compress_btn.isEnabled()
    assert compress_view.clear_btn.isEnabled()
    assert compress_view.file_info.isVisible()


def test_clear_file(compress_view):
    """Test clearing selected file."""
    compress_view._on_file_selected("test.pdf")
    compress_view._clear_file()
    
    assert compress_view.current_file is None
    assert not compress_view.file_info.isVisible()
    assert not compress_view.compress_btn.isEnabled()
    assert not compress_view.clear_btn.isEnabled()


def test_show_status_success(compress_view):
    """Test showing success status message."""
    compress_view._show_status("Test success", "success")
    
    assert compress_view.status_container.isVisible()
    assert "Test success" in compress_view.status_label.text()


def test_show_status_error(compress_view):
    """Test showing error status message."""
    compress_view._show_status("Test error", "error")
    
    assert compress_view.status_container.isVisible()
    assert "Test error" in compress_view.status_label.text()


def test_hide_status(compress_view):
    """Test hiding status message."""
    compress_view._show_status("Test", "info")
    assert compress_view.status_container.isVisible()
    
    compress_view._hide_status()
    assert not compress_view.status_container.isVisible()
