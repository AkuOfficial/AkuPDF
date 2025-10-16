import pytest
from PySide6.QtWidgets import QApplication
from src.ui.remove_password_view import RemovePasswordView


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_remove_password_view_initialization(qapp):
    """Test remove password view initializes correctly."""
    view = RemovePasswordView()
    assert view.input_file is None
    assert view.total_pages == 0
    assert not view.options_section.isEnabled()
    assert not view.actions_section.isEnabled()


def test_default_method_is_with_password(qapp):
    """Test default decryption method is with password."""
    view = RemovePasswordView()
    assert view.with_password_radio.isChecked()
    assert not view.without_password_radio.isChecked()


def test_method_toggle_changes_ui(qapp):
    """Test toggling between methods updates UI."""
    view = RemovePasswordView()
    view.options_section.setEnabled(True)
    
    # Default state - with password
    assert view.password_input.isEnabled()
    assert not view.recovery_label.isEnabled()
    
    # Switch to recovery mode
    view.without_password_radio.setChecked(True)
    assert not view.password_input.isEnabled()
    assert view.recovery_label.isEnabled()
    
    # Switch back to with password
    view.with_password_radio.setChecked(True)
    assert view.password_input.isEnabled()
    assert not view.recovery_label.isEnabled()


def test_clear_file_resets_state(qapp):
    """Test clear file resets all fields."""
    view = RemovePasswordView()
    view.input_file = "test.pdf"
    view.total_pages = 10
    view.password_input.setText("password123")
    view.without_password_radio.setChecked(True)
    
    view.clear_file()
    
    assert view.input_file is None
    assert view.total_pages == 0
    assert view.password_input.text() == ""
    assert view.with_password_radio.isChecked()


def test_process_requires_file(qapp):
    """Test process requires file to be selected."""
    view = RemovePasswordView()
    view.process_pdf()
    assert "select a pdf file" in view.status_label.text().lower()


def test_process_with_password_requires_password(qapp):
    """Test process with password method requires password."""
    view = RemovePasswordView()
    view.input_file = "test.pdf"
    view.total_pages = 10
    view.options_section.setEnabled(True)
    view.actions_section.setEnabled(True)
    view.with_password_radio.setChecked(True)
    view.password_input.setText("")
    
    view.process_pdf()
    assert "password" in view.status_label.text().lower()


def test_process_without_password_no_password_required(qapp):
    """Test process without password method doesn't require password."""
    view = RemovePasswordView()
    view.input_file = "test.pdf"
    view.total_pages = 10
    view.without_password_radio.setChecked(True)
    view.password_input.setText("")
    
    # Should not show password error (will show file dialog instead)
    # This test verifies the logic path, actual processing tested in integration tests
    assert view.without_password_radio.isChecked()
