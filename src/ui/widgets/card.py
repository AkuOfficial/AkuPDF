from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QSizePolicy,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QColor


class CardWidget(QFrame):
    """Modern card widget with qt-material base and custom styling."""

    def __init__(
        self,
        title: str,
        description: str,
        icon_text: str,
        click_handler: Callable[[], None],
    ):
        super().__init__()
        self._title = title
        self._description = description
        self._icon_text = icon_text
        self._click_handler = click_handler

        self._setup_ui()
        self._setup_shadow()

    def _setup_ui(self):
        """Initialize the card's UI components."""
        self.setFixedSize(280, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Icon
        icon_label = QLabel(self._icon_text)
        icon_label.setObjectName("cardIcon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(self._title)
        title_label.setObjectName("cardTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(self._description)
        desc_label.setObjectName("cardDescription")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        layout.addStretch()

        # Apply custom card styling
        self.setStyleSheet("""
            CardWidget {
                background: white;
                border-radius: 16px;
                border: 1px solid #e9ecef;
            }
            
            CardWidget:hover {
                border-color: #007bff;
                background: #f8f9ff;
            }
            
            QLabel#cardIcon {
                font-size: 48px;
                color: #007bff;
            }
            
            QLabel#cardTitle {
                font-size: 18px;
                font-weight: 600;
                color: #212529;
            }
            
            QLabel#cardDescription {
                font-size: 14px;
                color: #6c757d;
            }
        """)

    def _setup_shadow(self):
        """Add drop shadow effect."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if self._click_handler:
            self._click_handler()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Enhanced shadow on hover."""
        if self.graphicsEffect():
            shadow = self.graphicsEffect()
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 8)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Restore shadow on leave."""
        if self.graphicsEffect():
            shadow = self.graphicsEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 4)
        super().leaveEvent(event)
