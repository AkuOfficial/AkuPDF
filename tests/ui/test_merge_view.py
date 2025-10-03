import pytest
from PySide6.QtWidgets import QApplication
from src.ui.merge_view import MergeView


@pytest.fixture(scope="module")
def app():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def merge_view(app):
    """Create MergeView instance for tests."""
    view = MergeView()
    yield view


def test_merge_view_creation(merge_view):
    """Test that merge view is created successfully."""
    assert merge_view is not None


def test_merge_view_has_file_list(merge_view):
    """Test that file list widget exists."""
    assert merge_view.file_list is not None


def test_merge_view_initial_state(merge_view):
    """Test that merge view starts with empty file list."""
    assert len(merge_view.files) == 0
    assert merge_view.file_list.count() == 0


def test_clear_files(merge_view):
    """Test clearing files from the list."""
    merge_view.files = ["test1.pdf", "test2.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    
    merge_view.clear_files()
    
    assert len(merge_view.files) == 0
    assert merge_view.file_list.count() == 0


def test_remove_selected_file(merge_view):
    """Test removing a selected file from the list."""
    merge_view.files = ["test1.pdf", "test2.pdf", "test3.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    merge_view.file_list.addItem("test3.pdf")
    
    # Select second item
    merge_view.file_list.setCurrentRow(1)
    merge_view.remove_selected_file()
    
    assert len(merge_view.files) == 2
    assert merge_view.file_list.count() == 2
    assert "test2.pdf" not in merge_view.files


def test_back_callback(app):
    """Test that back callback is called."""
    callback_called = []
    
    def on_back_click():
        callback_called.append(True)
    
    view = MergeView(on_back_click=on_back_click)
    assert view is not None
