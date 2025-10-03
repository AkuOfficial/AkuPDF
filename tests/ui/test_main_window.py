import pytest
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


@pytest.fixture(scope="module")
def app():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def main_window(app):
    """Create MainWindow instance for tests."""
    window = MainWindow()
    yield window
    window.close()


def test_main_window_creation(main_window):
    """Test that main window is created successfully."""
    assert main_window is not None
    assert main_window.windowTitle() == "AkuPDF"


def test_main_window_size(main_window):
    """Test that main window has correct minimum size."""
    assert main_window.minimumWidth() == 1200
    assert main_window.minimumHeight() == 800


def test_sidebar_exists(main_window):
    """Test that sidebar is created."""
    assert main_window.sidebar is not None
    assert main_window.sidebar.width() == 280


def test_navigation_buttons_exist(main_window):
    """Test that navigation buttons are created."""
    assert main_window.home_btn is not None
    assert main_window.merge_btn is not None


def test_views_exist(main_window):
    """Test that views are created."""
    assert main_window.home_view is not None
    assert main_window.merge_view is not None
    assert main_window.stacked_widget.count() == 2


def test_initial_view_is_home(main_window):
    """Test that home view is shown initially."""
    assert main_window.stacked_widget.currentIndex() == 0


def test_switch_to_merge_view(main_window):
    """Test switching to merge view."""
    main_window._switch_view(1, main_window.merge_btn)
    assert main_window.stacked_widget.currentIndex() == 1


def test_switch_back_to_home(main_window):
    """Test switching back to home view."""
    main_window._switch_view(1, main_window.merge_btn)
    main_window._switch_view(0, main_window.home_btn)
    assert main_window.stacked_widget.currentIndex() == 0


def test_navigation_button_active_state(main_window):
    """Test that active button state is updated correctly."""
    main_window._switch_view(1, main_window.merge_btn)
    assert main_window.merge_btn.property("active")
    assert not main_window.home_btn.property("active")
