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
    yield view


def test_split_view_creation(split_view):
    """Test that split view is created successfully."""
    assert split_view is not None


def test_split_view_initial_state(split_view):
    """Test that split view starts with no file selected."""
    assert split_view.input_file is None
    assert "No file selected" in split_view.file_label.text()


def test_split_view_has_spinbox(split_view):
    """Test that split view has pages spinbox."""
    assert split_view.pages_spinbox is not None
    assert split_view.pages_spinbox.value() == 1
    assert split_view.pages_spinbox.minimum() == 1


def test_clear_file(split_view):
    """Test clearing selected file."""
    split_view.input_file = "test.pdf"
    split_view.file_label.setText("test.pdf")
    
    split_view.clear_file()
    
    assert split_view.input_file is None
    assert "No file selected" in split_view.file_label.text()


def test_back_callback(app):
    """Test that back callback is set."""
    callback_called = []
    
    def on_back_click():
        callback_called.append(True)
    
    view = SplitView(on_back_click=on_back_click)
    assert view is not None
