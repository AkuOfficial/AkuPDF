from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout

from src.ui.widgets.card import CardWidget


class HomeView(QWidget):
    """Futuristic home view."""

    def __init__(self, parent=None, on_merge_click=None, on_split_click=None, on_extract_click=None):
        super().__init__(parent)
        self._on_merge_click = on_merge_click
        self._on_split_click = on_split_click
        self._on_extract_click = on_extract_click
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Initialize the home view UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)

        # Welcome section
        welcome_section = self._create_welcome_section()
        layout.addWidget(welcome_section, 0, Qt.AlignmentFlag.AlignTop)

        # Feature cards grid
        cards_container = self._create_cards_grid()
        layout.addWidget(cards_container, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch(1)

    def _create_welcome_section(self):
        """Create the welcome section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("AKUPDF SUITE")
        title.setObjectName("welcomeTitle")
        layout.addWidget(title)

        subtitle = QLabel("NEXT-GENERATION PDF PROCESSING")
        subtitle.setObjectName("welcomeSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        return container

    def _create_cards_grid(self):
        """Create a grid layout with feature cards."""
        container = QWidget()
        container.setMaximumWidth(600)
        grid = QGridLayout(container)
        grid.setSpacing(24)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # Feature cards
        merge_card = CardWidget(
            "MERGE",
            "Combine multiple PDF files",
            "📄",
            self._on_merge_click,
        )
        grid.addWidget(merge_card, 0, 0)

        split_card = CardWidget(
            "SPLIT",
            "Extract and separate pages",
            "✂️",
            self._on_split_click,
        )
        grid.addWidget(split_card, 0, 1)

        extract_card = CardWidget(
            "EXTRACT",
            "Extract specific pages",
            "📑",
            self._on_extract_click,
        )
        grid.addWidget(extract_card, 1, 0)

        compress_card = CardWidget(
            "COMPRESS",
            "Optimize file size",
            "🗜️",
            lambda: None,
        )
        grid.addWidget(compress_card, 1, 1)

        return container

    def _apply_styles(self):
        """Apply futuristic styles."""
        self.setStyleSheet("""
            HomeView {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:1 #16213e);
            }
            
            QLabel#welcomeTitle {
                font-size: 36px;
                font-weight: 700;
                color: #00d9ff;
                letter-spacing: 4px;
            }
            
            QLabel#welcomeSubtitle {
                font-size: 14px;
                color: #8892b0;
                letter-spacing: 2px;
            }
        """)
