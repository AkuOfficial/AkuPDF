from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel, QGridLayout
from PySide6.QtGui import QFont

from src.ui.widgets.card import CardWidget


class HomeView(QWidget):
    """Modern home view with feature cards."""

    def __init__(self, parent=None, on_merge_click=None):
        super().__init__(parent)
        self._on_merge_click = on_merge_click
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Initialize the modern home view UI."""
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
        """Create the welcome section with title and description."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Main title
        title = QLabel("Welcome to AkuPDF")
        title.setObjectName("welcomeTitle")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Your complete PDF toolkit for merging, splitting, and managing documents")
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

        # Merge PDFs card
        merge_card = CardWidget(
            "Merge PDFs",
            "Combine multiple PDF files into a single document with ease",
            "📄",
            self._on_merge_click
        )
        grid.addWidget(merge_card, 0, 0)

        # Placeholder cards for future features
        split_card = CardWidget(
            "Split PDFs",
            "Extract specific pages or split documents into separate files",
            "✂️",
            lambda: None  # Placeholder
        )
        grid.addWidget(split_card, 0, 1)

        extract_card = CardWidget(
            "Extract Text",
            "Extract and export text content from your PDF documents",
            "📝",
            lambda: None  # Placeholder
        )
        grid.addWidget(extract_card, 1, 0)

        compress_card = CardWidget(
            "Compress PDFs",
            "Reduce file size while maintaining document quality",
            "🗜️",
            lambda: None  # Placeholder
        )
        grid.addWidget(compress_card, 1, 1)

        return container

    def _apply_styles(self):
        """Apply modern styles to the home view."""
        self.setStyleSheet("""
            HomeView {
                background: #f8f9fa;
            }
            
            #welcomeTitle {
                font-size: 32px;
                font-weight: 700;
                color: #212529;
                margin: 0;
            }
            
            #welcomeSubtitle {
                font-size: 16px;
                color: #6c757d;
                margin: 0;
                line-height: 1.5;
            }
        """)
