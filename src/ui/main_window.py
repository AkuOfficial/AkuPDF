from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QFrame,
    QLabel,
)

from src.ui.home_view import HomeView
from src.ui.merge_view import MergeView


class MainWindow(QMainWindow):
    """Main application window with Material Design sidebar."""

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        self._setup_views()

    def _setup_window(self):
        """Initialize window properties."""
        self.setWindowTitle("AkuPDF")
        self.setMinimumSize(900, 600)
        self.resize(1200, 800)

    def _setup_ui(self):
        """Set up the main UI with sidebar navigation."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create content area
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)

    def _create_sidebar(self):
        """Create Material Design sidebar."""
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setProperty("class", "sidebar")

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # App title section
        title_container = QWidget()
        title_container.setProperty("class", "title-container")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(24, 32, 24, 32)

        app_title = QLabel("AkuPDF")
        app_title.setProperty("class", "app-title")
        title_layout.addWidget(app_title)

        subtitle = QLabel("PDF Tools Suite")
        subtitle.setProperty("class", "app-subtitle")
        title_layout.addWidget(subtitle)

        layout.addWidget(title_container)

        # Navigation section
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(16, 24, 16, 0)
        nav_layout.setSpacing(8)

        self.home_btn = QPushButton("🏠  Home")
        self.merge_btn = QPushButton("📄  Merge PDFs")

        for btn in [self.home_btn, self.merge_btn]:
            btn.setProperty("class", "nav-button")

        self.home_btn.setProperty("active", True)
        self.home_btn.clicked.connect(lambda: self._switch_view(0, self.home_btn))
        self.merge_btn.clicked.connect(lambda: self._switch_view(1, self.merge_btn))

        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.merge_btn)
        nav_layout.addStretch()

        layout.addWidget(nav_container, 1)

        return sidebar

    def _setup_views(self):
        """Set up all views."""
        self.home_view = HomeView(
            self, on_merge_click=lambda: self._switch_view(1, self.merge_btn)
        )
        self.merge_view = MergeView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )

        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.merge_view)

    def _switch_view(self, index, button):
        """Switch to a different view and update navigation."""
        self.stacked_widget.setCurrentIndex(index)

        # Update button states
        for btn in [self.home_btn, self.merge_btn]:
            btn.setProperty("active", btn == button)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
