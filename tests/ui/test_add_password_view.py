import pytest
from PySide6.QtWidgets import QApplication
from src.ui.add_password_view import AddPasswordView


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_add_password_view_initialization(qapp):
    """Test add password view initializes correctly."""
    view = AddPasswordView()
    assert view.input_file is None
    assert view.total_pages == 0
    assert not view.options_section.isEnabled()
    assert not view.actions_section.isEnabled()


def test_user_password_field_exists(qapp):
    """Test user password field exists and is required."""
    view = AddPasswordView()
    assert view.user_password_input is not None
    assert view.user_password_input.placeholderText() == "Enter password to open the PDF"


def test_owner_password_field_exists(qapp):
    """Test owner password field exists and is optional."""
    view = AddPasswordView()
    assert view.owner_password_input is not None
    assert "empty" in view.owner_password_input.placeholderText().lower()


def test_clear_file_resets_state(qapp):
    """Test clear file resets all fields."""
    view = AddPasswordView()
    view.input_file = "test.pdf"
    view.total_pages = 10
    view.user_password_input.setText("password123")
    view.owner_password_input.setText("owner456")
    
    view.clear_file()
    
    assert view.input_file is None
    assert view.total_pages == 0
    assert view.user_password_input.text() == ""
    assert view.owner_password_input.text() == ""


def test_process_requires_file(qapp):
    """Test process requires file to be selected."""
    view = AddPasswordView()
    view.process_pdf()
    assert "select a pdf file" in view.status_label.text().lower()


def test_process_requires_user_password(qapp):
    """Test process requires user password."""
    view = AddPasswordView()
    view.input_file = "test.pdf"
    view.total_pages = 10
    view.options_section.setEnabled(True)
    view.actions_section.setEnabled(True)
    view.user_password_input.setText("")
    
    view.process_pdf()
    assert "password" in view.status_label.text().lower()
