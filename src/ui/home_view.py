from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame


class HomeView(QWidget):
    """Futuristic home view."""

    def __init__(self, parent=None, on_merge_click=None, on_split_click=None, on_extract_click=None, on_text_extract_click=None, on_image_extract_click=None):
        super().__init__(parent)
        self._on_merge_click = on_merge_click
        self._on_split_click = on_split_click
        self._on_extract_click = on_extract_click
        self._on_text_extract_click = on_text_extract_click
        self._on_image_extract_click = on_image_extract_click
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Initialize the home view UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setObjectName("scrollArea")
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)

        welcome_section = self._create_welcome_section()
        layout.addWidget(welcome_section, 0, Qt.AlignmentFlag.AlignTop)

        cards_container = self._create_cards_grid()
        layout.addWidget(cards_container, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch(1)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

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
        """Create getting started content."""
        container = QWidget()
        container.setMaximumWidth(700)
        layout = QVBoxLayout(container)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Getting Started Section
        intro = QLabel("Welcome to AkuPDF! Get started by selecting a feature below or from the sidebar.")
        intro.setObjectName("introText")
        intro.setWordWrap(True)
        layout.addWidget(intro)
        
        # Features List
        features = [
            ("📄 Merge PDFs", "Combine multiple PDF files into a single document", self._on_merge_click),
            ("✂️ Split PDF", "Separate a PDF into individual pages or ranges", self._on_split_click),
            ("📑 Extract Pages", "Extract specific pages from a PDF file", self._on_extract_click),
            ("📝 Extract Text", "Extract text content with layout preservation option", self._on_text_extract_click),
            ("🖼️ Extract Images", "Extract all images from PDF pages", self._on_image_extract_click)
        ]
        
        for icon_title, desc, handler in features:
            feature_frame = self._create_feature_item(icon_title, desc, handler)
            layout.addWidget(feature_frame)
        
        return container
    
    def _create_feature_item(self, title, description, click_handler):
        """Create a clickable feature list item."""
        frame = QFrame()
        frame.setObjectName("featureFrame")
        frame.setCursor(Qt.CursorShape.PointingHandCursor)
        frame.mousePressEvent = lambda e: click_handler() if click_handler else None
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setObjectName("featureTitle")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setObjectName("featureDesc")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return frame

    def _apply_styles(self):
        """Apply futuristic styles."""
        self.setStyleSheet("""
            HomeView {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:1 #16213e);
            }
            
            QScrollArea#scrollArea {
                background: transparent;
                border: none;
            }
            
            QScrollArea#scrollArea > QWidget {
                background: transparent;
            }
            
            QScrollArea#scrollArea QScrollBar:vertical {
                background: #0a0e27;
                width: 12px;
                border: 1px solid #00d9ff;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollArea#scrollArea QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #00b8d4);
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollArea#scrollArea QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00f0ff, stop:1 #00d9ff);
            }
            
            QScrollArea#scrollArea QScrollBar::add-line:vertical,
            QScrollArea#scrollArea QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollArea#scrollArea QScrollBar::add-page:vertical,
            QScrollArea#scrollArea QScrollBar::sub-page:vertical {
                background: none;
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
            
            QLabel#introText {
                font-size: 16px;
                color: #8892b0;
                line-height: 1.6;
                margin-bottom: 12px;
            }
            
            QFrame#featureFrame {
                background: rgba(26, 31, 58, 0.6);
                border: 1px solid rgba(0, 217, 255, 0.2);
                border-radius: 8px;
            }
            
            QFrame#featureFrame:hover {
                background: rgba(0, 217, 255, 0.08);
                border-color: rgba(0, 217, 255, 0.4);
            }
            
            QLabel#featureTitle {
                font-size: 15px;
                font-weight: 600;
                color: #00d9ff;
            }
            
            QLabel#featureDesc {
                font-size: 13px;
                color: #8892b0;
                line-height: 1.5;
            }
        """)
