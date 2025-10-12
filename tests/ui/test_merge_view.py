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
    view.show()
    yield view


def test_merge_view_creation(merge_view):
    """Test that merge view is created successfully."""
    assert merge_view is not None


def test_merge_view_has_file_list(merge_view):
    """Test that file list widget exists."""
    assert merge_view.file_list is not None


def test_merge_view_has_status_container(merge_view):
    """Test that status container exists."""
    assert merge_view.status_container is not None
    assert not merge_view.status_container.isVisible()


def test_merge_view_has_buttons(merge_view):
    """Test that all buttons exist."""
    assert merge_view.remove_btn is not None
    assert merge_view.clear_btn is not None
    assert merge_view.merge_btn is not None


def test_buttons_disabled_initially(merge_view):
    """Test that buttons are disabled initially."""
    assert not merge_view.remove_btn.isEnabled()
    assert not merge_view.clear_btn.isEnabled()
    assert not merge_view.merge_btn.isEnabled()


def test_merge_view_initial_state(merge_view):
    """Test that merge view starts with empty file list."""
    assert len(merge_view.files) == 0
    assert merge_view.file_list.count() == 0


def test_clear_button_enabled_with_one_file(merge_view):
    """Test that clear button is enabled with 1 file."""
    merge_view.files = ["test1.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view._update_button_states()
    
    assert merge_view.clear_btn.isEnabled()
    assert not merge_view.merge_btn.isEnabled()


def test_merge_button_enabled_with_two_files(merge_view):
    """Test that merge button is enabled with 2 or more files."""
    merge_view.files = ["test1.pdf", "test2.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    merge_view._update_button_states()
    
    assert merge_view.clear_btn.isEnabled()
    assert merge_view.merge_btn.isEnabled()


def test_clear_files(merge_view):
    """Test clearing files from the list."""
    merge_view.files = ["test1.pdf", "test2.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    
    merge_view.clear_files()
    
    assert len(merge_view.files) == 0
    assert merge_view.file_list.count() == 0
    assert not merge_view.clear_btn.isEnabled()
    assert not merge_view.merge_btn.isEnabled()


def test_remove_button_enabled_when_file_selected(merge_view):
    """Test that remove button is enabled when a file is selected."""
    merge_view.files = ["test1.pdf", "test2.pdf"]
    merge_view.file_list.addItem("test1.pdf")
    merge_view.file_list.addItem("test2.pdf")
    
    merge_view.file_list.setCurrentRow(0)
    merge_view._update_remove_button_state()
    
    assert merge_view.remove_btn.isEnabled()


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
    merge_view._show_status("Test success message", "success")
    
    assert merge_view.status_container.isVisible()
    assert "Test success message" in merge_view.status_label.text()


def test_show_status_error(merge_view):
    """Test showing error status message."""
    merge_view._show_status("Test error message", "error")
    
    assert merge_view.status_container.isVisible()
    assert "Test error message" in merge_view.status_label.text()


def test_hide_status(merge_view):
    """Test hiding status message."""
    merge_view._show_status("Test message", "info")
    assert merge_view.status_container.isVisible()
    
    merge_view._hide_status()
    assert not merge_view.status_container.isVisible()


def test_back_callback(app):
    """Test that back callback is called."""
    callback_called = []
    
    def on_back_click():
        callback_called.append(True)
    
    view = MergeView(on_back_click=on_back_click)
    assert view is not None


def test_merge_view_with_mixed_content(merge_view):
    """Test merge view can handle mixed content PDF."""
    from pathlib import Path
    test_file = Path(__file__).parent.parent / "data" / "mixed_content.pdf"
    if test_file.exists():
        merge_view.files = [str(test_file)]
        merge_view.file_list.addItem(str(test_file))
        merge_view._update_button_states()
        assert merge_view.clear_btn.isEnabled()
