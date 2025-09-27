from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                QPushButton, QStackedWidget, QFrame, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.ui.home_view import HomeView
from src.ui.merge_view import MergeView


class MainWindow(QMainWindow):
    """Main application window with modern sidebar navigation."""

    APPLICATION_NAME = "AkuPDF"

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        self._setup_views()
        self._apply_styles()

    def _setup_window(self):
        """Initialize window properties."""
        self.setWindowTitle(self.APPLICATION_NAME)
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

    def _setup_ui(self):
        """Set up the main UI with sidebar navigation."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main horizontal layout
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
        """Create modern sidebar navigation."""
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # App title
        title_container = QWidget()
        title_container.setObjectName("titleContainer")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(24, 32, 24, 32)
        
        app_title = QLabel("AkuPDF")
        app_title.setObjectName("appTitle")
        title_layout.addWidget(app_title)
        
        subtitle = QLabel("PDF Tools Suite")
        subtitle.setObjectName("appSubtitle")
        title_layout.addWidget(subtitle)
        
        layout.addWidget(title_container)

        # Navigation buttons
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(16, 0, 16, 0)
        nav_layout.setSpacing(8)

        self.home_btn = self._create_nav_button("🏠  Home", True)
        self.merge_btn = self._create_nav_button("📄  Merge PDFs", False)
        
        self.home_btn.clicked.connect(lambda: self._switch_view(0, self.home_btn))
        self.merge_btn.clicked.connect(lambda: self._switch_view(1, self.merge_btn))

        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.merge_btn)
        nav_layout.addStretch()
        
        layout.addWidget(nav_container, 1)
        
        return sidebar

    def _create_nav_button(self, text, active=False):
        """Create a navigation button."""
        btn = QPushButton(text)
        btn.setObjectName("navButton")
        if active:
            btn.setProperty("active", True)
        return btn

    def _setup_views(self):
        """Set up all views."""
        self.home_view = HomeView(self, on_merge_click=lambda: self._switch_view(1, self.merge_btn))
        self.merge_view = MergeView(on_back_click=lambda: self._switch_view(0, self.home_btn))
        
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

    def _apply_styles(self):
        """Apply modern styles to the main window."""
        self.setStyleSheet("""
            QMainWindow {
                background: #f8f9fa;
            }
            
            #sidebar {
                background: #ffffff;
                border-right: 1px solid #e9ecef;
            }
            
            #titleContainer {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
            }
            
            #appTitle {
                font-size: 24px;
                font-weight: 700;
                color: white;
                margin: 0;
            }
            
            #appSubtitle {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.8);
                margin: 0;
            }
            
            #navButton {
                text-align: left;
                padding: 16px 20px;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 500;
                color: #495057;
                background: transparent;
                margin: 2px 0;
            }
            
            #navButton:hover {
                background: #f8f9fa;
                color: #212529;
            }
            
            #navButton[active="true"] {
                background: #e3f2fd;
                color: #1976d2;
                font-weight: 600;
            }
            
            QStackedWidget {
                background: #f8f9fa;
            }
        """)
