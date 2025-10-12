import pytest
from PySide6.QtWidgets import QApplication, QLabel, QFrame
from PySide6.QtCore import Qt
from src.ui.home_view import HomeView


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


def test_home_view_has_feature_frames(home_view):
    """Test that home view has feature frames."""
    frames = [f for f in home_view.findChildren(QFrame) if f.objectName() == "featureFrame"]
    assert len(frames) == 5


def test_merge_click_callback(app):
    """Test that merge click callback works."""
    callback_called = []

    def on_merge_click():
        callback_called.append(True)

    view = HomeView(on_merge_click=on_merge_click)
    frames = [f for f in view.findChildren(QFrame) if f.objectName() == "featureFrame"]
    assert len(frames) > 0
    
    frames[0].mousePressEvent(None)
    assert len(callback_called) == 1


def test_extract_click_callback(app):
    """Test that extract click callback works."""
    callback_called = []

    def on_extract_click():
        callback_called.append(True)

    view = HomeView(on_extract_click=on_extract_click)
    frames = [f for f in view.findChildren(QFrame) if f.objectName() == "featureFrame"]
    assert len(frames) >= 3
    
    frames[2].mousePressEvent(None)
    assert len(callback_called) == 1


def test_feature_frames_have_cursor(home_view):
    """Test that feature frames have pointer cursor."""
    frames = [f for f in home_view.findChildren(QFrame) if f.objectName() == "featureFrame"]
    for frame in frames:
        assert frame.cursor().shape() == Qt.CursorShape.PointingHandCursor
