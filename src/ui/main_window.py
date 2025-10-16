from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QFrame,
    QLabel,
    QScrollArea,
)
from PySide6.QtCore import Qt

from src.ui.home_view import HomeView
from src.ui.merge_view import MergeView
from src.ui.split_view import SplitView
from src.ui.extract_pages_view import ExtractView
from src.ui.text_extract_view import TextExtractView
from src.ui.image_extract_view import ImageExtractView
from src.ui.compress_view import CompressView
from src.ui.pdf_to_docx_view import PdfToDocxView
from src.ui.pdf_to_xlsx_view import PdfToXlsxView
from src.ui.pdf_to_images_view import PdfToImagesView
from src.ui.watermark_view import WatermarkView
from src.ui.add_password_view import AddPasswordView
from src.ui.remove_password_view import RemovePasswordView


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
        self.setMinimumSize(950, 650)
        self.resize(1000, 650)

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

        # Scrollable navigation section
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setProperty("class", "sidebar-scroll")
        
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(16, 24, 16, 16)
        nav_layout.setSpacing(8)

        self.home_btn = QPushButton("🏠  Home")
        self.home_btn.setProperty("class", "nav-button")
        self.home_btn.setProperty("active", True)
        self.home_btn.clicked.connect(lambda: self._switch_view(0, self.home_btn))
        nav_layout.addWidget(self.home_btn)
        
        # Basic Operations Group
        basic_label = QLabel("BASIC OPERATIONS")
        basic_label.setProperty("class", "nav-group-label")
        nav_layout.addWidget(basic_label)
        
        self.merge_btn = QPushButton("📄  Merge PDFs")
        self.split_btn = QPushButton("✂️  Split PDFs")
        self.extract_btn = QPushButton("📑  Extract Pages")
        self.compress_btn = QPushButton("🗜️  Compress PDF")
        self.watermark_btn = QPushButton("💧  Add Watermark")
        self.add_password_btn = QPushButton("🔒  Add Password")
        self.remove_password_btn = QPushButton("🔓  Remove Password")
        
        for btn in [self.merge_btn, self.split_btn, self.extract_btn, self.compress_btn, self.watermark_btn, self.add_password_btn, self.remove_password_btn]:
            btn.setProperty("class", "nav-button")
        
        self.merge_btn.clicked.connect(lambda: self._switch_view(1, self.merge_btn))
        self.split_btn.clicked.connect(lambda: self._switch_view(2, self.split_btn))
        self.extract_btn.clicked.connect(lambda: self._switch_view(3, self.extract_btn))
        self.compress_btn.clicked.connect(lambda: self._switch_view(4, self.compress_btn))
        self.watermark_btn.clicked.connect(lambda: self._switch_view(10, self.watermark_btn))
        self.add_password_btn.clicked.connect(lambda: self._switch_view(11, self.add_password_btn))
        self.remove_password_btn.clicked.connect(lambda: self._switch_view(12, self.remove_password_btn))
        
        nav_layout.addWidget(self.merge_btn)
        nav_layout.addWidget(self.split_btn)
        nav_layout.addWidget(self.extract_btn)
        nav_layout.addWidget(self.compress_btn)
        nav_layout.addWidget(self.watermark_btn)
        nav_layout.addWidget(self.add_password_btn)
        nav_layout.addWidget(self.remove_password_btn)
        
        # Content Extraction Group
        extract_label = QLabel("CONTENT EXTRACTION")
        extract_label.setProperty("class", "nav-group-label")
        nav_layout.addWidget(extract_label)
        
        self.text_extract_btn = QPushButton("📝  Extract Text")
        self.image_extract_btn = QPushButton("🖼️  Extract Images")
        
        for btn in [self.text_extract_btn, self.image_extract_btn]:
            btn.setProperty("class", "nav-button")
        
        self.text_extract_btn.clicked.connect(lambda: self._switch_view(5, self.text_extract_btn))
        self.image_extract_btn.clicked.connect(lambda: self._switch_view(6, self.image_extract_btn))
        
        nav_layout.addWidget(self.text_extract_btn)
        nav_layout.addWidget(self.image_extract_btn)
        
        # Conversion Group
        convert_label = QLabel("CONVERSION")
        convert_label.setProperty("class", "nav-group-label")
        nav_layout.addWidget(convert_label)
        
        self.docx_btn = QPushButton("📄  PDF to DOCX")
        self.xlsx_btn = QPushButton("📊  PDF to XLSX")
        self.images_btn = QPushButton("🖼️  PDF to Images")
        
        for btn in [self.docx_btn, self.xlsx_btn, self.images_btn]:
            btn.setProperty("class", "nav-button")
        
        self.docx_btn.clicked.connect(lambda: self._switch_view(7, self.docx_btn))
        self.xlsx_btn.clicked.connect(lambda: self._switch_view(8, self.xlsx_btn))
        self.images_btn.clicked.connect(lambda: self._switch_view(9, self.images_btn))
        
        nav_layout.addWidget(self.docx_btn)
        nav_layout.addWidget(self.xlsx_btn)
        nav_layout.addWidget(self.images_btn)
        
        nav_layout.addStretch()

        scroll_area.setWidget(nav_container)
        layout.addWidget(scroll_area, 1)

        return sidebar

    def _setup_views(self):
        """Set up all views."""
        self.home_view = HomeView(
            self,
            on_merge_click=lambda: self._switch_view(1, self.merge_btn),
            on_split_click=lambda: self._switch_view(2, self.split_btn),
            on_extract_click=lambda: self._switch_view(3, self.extract_btn),
            on_text_extract_click=lambda: self._switch_view(5, self.text_extract_btn),
            on_image_extract_click=lambda: self._switch_view(6, self.image_extract_btn)
        )
        self.merge_view = MergeView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.split_view = SplitView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.extract_view = ExtractView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.text_extract_view = TextExtractView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.image_extract_view = ImageExtractView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.compress_view = CompressView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.docx_view = PdfToDocxView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.xlsx_view = PdfToXlsxView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.images_view = PdfToImagesView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.watermark_view = WatermarkView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.add_password_view = AddPasswordView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )
        self.remove_password_view = RemovePasswordView(
            on_back_click=lambda: self._switch_view(0, self.home_btn)
        )

        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.merge_view)
        self.stacked_widget.addWidget(self.split_view)
        self.stacked_widget.addWidget(self.extract_view)
        self.stacked_widget.addWidget(self.compress_view)
        self.stacked_widget.addWidget(self.text_extract_view)
        self.stacked_widget.addWidget(self.image_extract_view)
        self.stacked_widget.addWidget(self.docx_view)
        self.stacked_widget.addWidget(self.xlsx_view)
        self.stacked_widget.addWidget(self.images_view)
        self.stacked_widget.addWidget(self.watermark_view)
        self.stacked_widget.addWidget(self.add_password_view)
        self.stacked_widget.addWidget(self.remove_password_view)

    def _switch_view(self, index, button):
        """Switch to a different view and update navigation."""
        self.stacked_widget.setCurrentIndex(index)

        # Update button states
        for btn in [self.home_btn, self.merge_btn, self.split_btn, self.extract_btn, self.compress_btn, self.watermark_btn, self.add_password_btn, self.remove_password_btn, self.text_extract_btn, self.image_extract_btn, self.docx_btn, self.xlsx_btn, self.images_btn]:
            btn.setProperty("active", btn == button)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
