from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HeaderWidget(QWidget):
    """Header widget with title and subtitle."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the header UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self._add_title(layout)
        self._add_subtitle(layout)

    def _add_title(self, parent_layout):
        """Add title to the header."""
        title = QLabel("AkuPDF Tools")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 600;
                color: #2c3e50;
                padding: 10px 0;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(title)

    def _add_subtitle(self, parent_layout):
        """Add subtitle to the header."""
        subheader = QLabel("Select an action to get started")
        subheader.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #7f8c8d;
                padding-bottom: 20px;
            }
        """)
        subheader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(subheader)
