from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QSizePolicy, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


class CardWidget(QFrame):
    """Futuristic card widget with neon glow effects."""

    def __init__(self, title: str, description: str, icon_text: str, click_handler: Callable[[], None]):
        super().__init__()
        self._title = title
        self._description = description
        self._icon_text = icon_text
        self._click_handler = click_handler

        self._setup_ui()
        self._setup_glow()

    def _setup_ui(self):
        """Initialize the card's UI components."""
        self.setFixedSize(240, 180)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)
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

        # Apply futuristic card styling
        self.setStyleSheet("""
            CardWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(26, 31, 58, 0.8), stop:1 rgba(15, 23, 41, 0.8));
                border: 2px solid rgba(0, 217, 255, 0.3);
                border-radius: 16px;
            }
            
            CardWidget:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 217, 255, 0.15), stop:1 rgba(123, 44, 191, 0.15));
                border-color: #00d9ff;
            }
            
            QLabel#cardIcon {
                font-size: 48px;
                color: #00d9ff;
            }
            
            QLabel#cardTitle {
                font-size: 18px;
                font-weight: 700;
                color: #00d9ff;
                letter-spacing: 2px;
            }
            
            QLabel#cardDescription {
                font-size: 12px;
                color: #8892b0;
                letter-spacing: 1px;
            }
        """)

    def _setup_glow(self):
        """Add neon glow effect."""
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setColor(QColor(0, 217, 255, 80))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if self._click_handler:
            self._click_handler()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Enhanced glow on hover."""
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setBlurRadius(40)
            effect.setColor(QColor(0, 217, 255, 120))
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Restore glow on leave."""
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setBlurRadius(30)
            effect.setColor(QColor(0, 217, 255, 80))
        super().leaveEvent(event)
