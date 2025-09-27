from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QSizePolicy, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


class CardWidget(QFrame):
    """Modern clickable card widget with smooth hover effects."""

    def __init__(self, title: str, description: str, icon_text: str, click_handler: Callable[[], None]):
        super().__init__()
        self._title = title
        self._description = description
        self._icon_text = icon_text
        self._click_handler = click_handler

        self._setup_ui()
        self._setup_styles()
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

        self._add_icon(layout)
        self._add_title(layout)
        self._add_description(layout)
        layout.addStretch()

    def _setup_shadow(self):
        """Add drop shadow effect."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def _setup_styles(self):
        """Apply modern card styles."""
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
                margin: 0;
            }
            
            QLabel#cardTitle {
                font-size: 18px;
                font-weight: 600;
                color: #212529;
                margin: 0;
            }
            
            QLabel#cardDescription {
                font-size: 14px;
                color: #6c757d;
                line-height: 1.4;
                margin: 0;
            }
        """)

    def _add_icon(self, parent_layout):
        """Add emoji icon to the card."""
        icon_label = QLabel(self._icon_text)
        icon_label.setObjectName("cardIcon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(icon_label)

    def _add_title(self, parent_layout):
        """Add title to the card."""
        title_label = QLabel(self._title)
        title_label.setObjectName("cardTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        parent_layout.addWidget(title_label)

    def _add_description(self, parent_layout):
        """Add description to the card."""
        desc_label = QLabel(self._description)
        desc_label.setObjectName("cardDescription")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        parent_layout.addWidget(desc_label)

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if self._click_handler:
            self._click_handler()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Handle mouse enter events for enhanced shadow."""
        if self.graphicsEffect():
            shadow = self.graphicsEffect()
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 8)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave events to restore shadow."""
        if self.graphicsEffect():
            shadow = self.graphicsEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 4)
        super().leaveEvent(event)