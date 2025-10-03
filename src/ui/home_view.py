from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout

from src.ui.widgets.card import CardWidget


class HomeView(QWidget):
    """Modern home view with custom styling over qt-material base."""

    def __init__(self, parent=None, on_merge_click=None):
        super().__init__(parent)
        self._on_merge_click = on_merge_click
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Initialize the home view UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)

        # Welcome section
        welcome_section = self._create_welcome_section()
        layout.addWidget(welcome_section)

        # Feature cards grid
        cards_container = self._create_cards_grid()
        layout.addWidget(cards_container, 1)

        layout.addStretch()

    def _create_welcome_section(self):
        """Create the welcome section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Welcome to AkuPDF")
        title.setObjectName("welcomeTitle")
        layout.addWidget(title)

        subtitle = QLabel(
            "Your complete PDF toolkit for merging, splitting, and managing documents"
        )
        subtitle.setObjectName("welcomeSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        return container

    def _create_cards_grid(self):
        """Create a grid layout with feature cards."""
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(24)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Feature cards
        merge_card = CardWidget(
            "Merge PDFs",
            "Combine multiple PDF files into a single document with ease",
            "📄",
            self._on_merge_click,
        )
        grid.addWidget(merge_card, 0, 0)

        split_card = CardWidget(
            "Split PDFs",
            "Extract specific pages or split documents into separate files",
            "✂️",
            lambda: None,
        )
        grid.addWidget(split_card, 0, 1)

        extract_card = CardWidget(
            "Extract Text",
            "Extract and export text content from your PDF documents",
            "📝",
            lambda: None,
        )
        grid.addWidget(extract_card, 1, 0)

        compress_card = CardWidget(
            "Compress PDFs",
            "Reduce file size while maintaining document quality",
            "🗜️",
            lambda: None,
        )
        grid.addWidget(compress_card, 1, 1)

        return container

    def _apply_styles(self):
        """Apply custom styles over qt-material base."""
        self.setStyleSheet("""
            HomeView {
                background: #f8f9fa;
            }
            
            QLabel#welcomeTitle {
                font-size: 32px;
                font-weight: 700;
                color: #212529;
            }
            
            QLabel#welcomeSubtitle {
                font-size: 16px;
                color: #6c757d;
            }
        """)
