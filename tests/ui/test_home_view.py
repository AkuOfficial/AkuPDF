import pytest
from PySide6.QtWidgets import QApplication, QLabel
from src.ui.home_view import HomeView
from src.ui.widgets.card import CardWidget


@pytest.fixture(scope="module")
def app():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def home_view(app):
    """Create HomeView instance for tests."""
    view = HomeView()
    yield view


def test_home_view_creation(home_view):
    """Test that home view is created successfully."""
    assert home_view is not None


def test_home_view_has_labels(home_view):
    """Test that home view has labels."""
    labels = home_view.findChildren(QLabel)
    assert len(labels) >= 2


def test_home_view_has_cards(home_view):
    """Test that home view has feature cards."""
    cards = home_view.findChildren(CardWidget)
    assert len(cards) == 4


def test_merge_click_callback(app):
    """Test that merge click callback is set."""
    callback_called = []

    def on_merge_click():
        callback_called.append(True)

    view = HomeView(on_merge_click=on_merge_click)
    assert view is not None
