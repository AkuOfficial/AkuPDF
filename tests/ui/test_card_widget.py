import pytest
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QMouseEvent
from src.ui.widgets.card import CardWidget


@pytest.fixture(scope="module")
def app():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def card_widget(app):
    """Create CardWidget instance for tests."""

    def dummy_handler():
        pass

    card = CardWidget("Test Card", "Test description", "🧪", dummy_handler)
    yield card


def test_card_widget_creation(card_widget):
    """Test that card widget is created successfully."""
    assert card_widget is not None


def test_card_widget_size(card_widget):
    """Test that card widget has correct size."""
    assert card_widget.width() == 240
    assert card_widget.height() == 180


def test_card_widget_cursor(card_widget):
    """Test that card widget has pointing hand cursor."""
    assert card_widget.cursor().shape() == Qt.CursorShape.PointingHandCursor


def test_card_click_handler(app):
    """Test that click handler is called when card is clicked."""
    clicked = []

    def click_handler():
        clicked.append(True)

    card = CardWidget("Test", "Description", "🧪", click_handler)

    # Simulate mouse press with proper QMouseEvent
    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(10, 10),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    card.mousePressEvent(event)

    assert len(clicked) == 1


def test_card_has_labels(card_widget):
    """Test that card has icon, title, and description labels."""
    labels = card_widget.findChildren(QLabel)
    assert len(labels) == 3
