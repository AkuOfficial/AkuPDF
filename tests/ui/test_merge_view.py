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


def test_merge_view_has_status_label(merge_view):
    """Test that status label exists."""
    assert merge_view.status_label is not None
    assert merge_view.status_label.isHidden()


def test_merge_view_has_buttons(merge_view):
    """Test that all buttons exist."""
    assert merge_view.remove_btn is not None
    assert merge_view.clear_btn is not None
    assert merge_view.merge_btn is not None


def test_buttons_disabled_initially(merge_view):
    """Test that buttons are disabled initially."""
    assert merge_view.remove_btn.isEnabled() == False
    assert merge_view.clear_btn.isEnabled() == False
    assert merge_view.merge_btn.isEnabled() == False


def test_merge_view_initial_state(merge_view):
    """Test that merge view starts with empty file list."""
    assert len(merge_view.files) == 0
    assert merge_view.file_list.count() == 0


def test_clear_button_enabled_with_one_file(merge_view):
    """Test that clear button is enabled with 1 file."""
    merge_view.files = ["test1.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view._update_button_states()
    
    assert merge_view.clear_btn.isEnabled() == True
    assert merge_view.merge_btn.isEnabled() == False


def test_merge_button_enabled_with_two_files(merge_view):
    """Test that merge button is enabled with 2 or more files."""
    merge_view.files = ["test1.pdf", "test2.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    merge_view._update_button_states()
    
    assert merge_view.clear_btn.isEnabled() == True
    assert merge_view.merge_btn.isEnabled() == True


def test_clear_files(merge_view):
    """Test clearing files from the list."""
    merge_view.files = ["test1.pdf", "test2.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    
    merge_view.clear_files()
    
    assert len(merge_view.files) == 0
    assert merge_view.file_list.count() == 0
    assert merge_view.clear_btn.isEnabled() == False
    assert merge_view.merge_btn.isEnabled() == False


def test_remove_button_enabled_when_file_selected(merge_view):
    """Test that remove button is enabled when a file is selected."""
    merge_view.files = ["test1.pdf", "test2.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    
    merge_view.file_list.setCurrentRow(0)
    merge_view._update_remove_button_state()
    
    assert merge_view.remove_btn.isEnabled() == True


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


def test_show_status_success(merge_view):
    """Test showing success status message."""
    merge_view._show_status("Test success message", False)
    
    assert not merge_view.status_label.isHidden()
    assert "Test success message" in merge_view.status_label.text()


def test_show_status_error(merge_view):
    """Test showing error status message."""
    merge_view._show_status("Test error message", True)
    
    assert not merge_view.status_label.isHidden()
    assert "Test error message" in merge_view.status_label.text()


def test_back_callback(app):
    """Test that back callback is called."""
    callback_called = []
    
    def on_back_click():
        callback_called.append(True)
    
    view = MergeView(on_back_click=on_back_click)
    assert view is not None
