"""Theme configuration for the application."""
import qdarkstyle
from PySide6.QtGui import QIcon, QPainter


def apply_theme(app):
    """Apply the dark theme to the application.
    
    Args:
        app: The QApplication instance.
    """
    # Apply the dark stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    
    # Set a consistent font
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)


def create_icon(name, color=None):
    """Create an icon with the specified name and optional color.
    
    Args:
        name: The name of the icon (from the current theme).
        color: Optional color to apply to the icon.
        
    Returns:
        QIcon: The created icon.
    """
    icon = QIcon.fromTheme(name)
    if icon.isNull():
        # Fallback to a default icon if theme icon is not found
        return QIcon()
    
    if color:
        # Apply color to the icon if specified
        pixmap = icon.pixmap(32, 32)
        if not pixmap.isNull():
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), color)
            painter.end()
            return QIcon(pixmap)
    
    return icon
