from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QFrame, QLineEdit
)
from PySide6.QtCore import Qt
from src.modules.split import Splitter
from src.modules.pdf_utils import parse_page_numbers, get_pdf_info
from src.ui.widgets.drop_zone import DropZone


class ExtractView(QWidget):
    """Futuristic extract pages view."""

    def __init__(self, on_back_click=None):
        super().__init__()
        self._on_back_click = on_back_click
        self.input_file = None
        self.total_pages = 0
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Set up the extract view UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(16)

        # Header
        header = self._create_header()
        layout.addWidget(header)

        # Status message container
        self.status_container = QWidget()
        self.status_container.setObjectName("statusContainer")
        self.status_container.setMaximumHeight(60)
        status_layout = QHBoxLayout(self.status_container)
        status_layout.setContentsMargins(12, 12, 12, 12)
        status_layout.setSpacing(8)
        
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label, 1)
        
        self.status_close_btn = QPushButton("✕")
        self.status_close_btn.setObjectName("statusCloseBtn")
        self.status_close_btn.setFixedSize(24, 24)
        self.status_close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.status_close_btn.clicked.connect(self._hide_status)
        status_layout.addWidget(self.status_close_btn)
        
        self.status_container.hide()
        layout.addWidget(self.status_container)

        # File section
        file_section = self._create_file_section()
        layout.addWidget(file_section)

        # Options section
        self.options_section = self._create_options_section()
        self.options_section.setEnabled(False)
        layout.addWidget(self.options_section)

        # Actions
        self.actions_section = self._create_actions()
        self.actions_section.setEnabled(False)
        layout.addWidget(self.actions_section)

    @staticmethod
    def _create_header():
        """Create the header section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Extract PDF Pages")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        subtitle = QLabel("Extract specific pages from a PDF document")
        subtitle.setObjectName("sectionSubtitle")
        layout.addWidget(subtitle)

        return container

    def _create_file_section(self):
        """Create the file selection section."""
        container = QFrame()
        container.setProperty("class", "file-section")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.filesDropped.connect(self._handle_dropped_file)
        layout.addWidget(self.drop_zone)

        self.file_info_container = QWidget()
        file_info_layout = QVBoxLayout(self.file_info_container)
        file_info_layout.setContentsMargins(0, 0, 0, 0)
        file_info_layout.setSpacing(8)

        list_header = QLabel("INPUT FILE")
        list_header.setProperty("class", "list-header")
        file_info_layout.addWidget(list_header)

        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileLabel")
        self.file_label.setWordWrap(True)
        file_info_layout.addWidget(self.file_label)

        self.page_info_label = QLabel("")
        self.page_info_label.setObjectName("pageInfoLabel")
        file_info_layout.addWidget(self.page_info_label)

        self.file_info_container.hide()
        layout.addWidget(self.file_info_container)

        return container

    def _create_options_section(self):
        """Create the options section."""
        container = QFrame()
        container.setProperty("class", "file-section")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        options_header = QLabel("OPTIONS")
        options_header.setProperty("class", "list-header")
        layout.addWidget(options_header)

        # Extract: Page numbers input
        extract_label = QLabel("Page numbers (e.g., 1,3,5-7):")
        extract_label.setObjectName("optionLabel")
        layout.addWidget(extract_label)
        
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Enter page numbers...")
        layout.addWidget(self.pages_input)

        return container

    def _create_actions(self):
        """Create the action buttons section."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(16)

        clear_btn = QPushButton("CLEAR")
        clear_btn.setProperty("class", "secondary-button")
        clear_btn.clicked.connect(self.clear_file)
        layout.addWidget(clear_btn)

        layout.addStretch()

        extract_btn = QPushButton("📄  EXTRACT PAGES")
        extract_btn.setProperty("class", "primary-button")
        extract_btn.clicked.connect(self.extract_pages)
        layout.addWidget(extract_btn)

        return container

    def _show_status(self, message, status_type="info"):
        """Show status message inline."""
        self.status_label.setText(message)
        self.status_container.setProperty("statusType", status_type)
        self.status_container.style().unpolish(self.status_container)
        self.status_container.style().polish(self.status_container)
        self.status_container.show()
    
    def _hide_status(self):
        """Hide status message."""
        self.status_container.hide()



    def _handle_dropped_file(self, files):
        """Handle file dropped into drop zone."""
        self._hide_status()
        if not files:
            self.select_file()
            return
        if files:
            self._load_file(files[0])

    def _load_file(self, file):
        """Load PDF file and update UI."""
        try:
            pdf_info = get_pdf_info(file)
            self.total_pages = pdf_info['total_pages']
            
            if self.total_pages == 0:
                self._show_status("⚠️ The selected PDF has no pages.", "error")
                return
            
            self.input_file = file
            self.file_label.setText(file)
            self.page_info_label.setText(f"Total pages: {self.total_pages}")
            
            self.drop_zone.hide()
            self.file_info_container.show()
            self.options_section.setEnabled(True)
            self.actions_section.setEnabled(True)
            
        except Exception as e:
            self._show_status(f"❌ Failed to read PDF: {str(e)}", "error")

    def select_file(self):
        """Select input PDF file."""
        file, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file:
            self._load_file(file)

    def clear_file(self):
        """Clear selected file."""
        self._hide_status()
        self.input_file = None
        self.total_pages = 0
        self.file_label.setText("No file selected")
        self.page_info_label.setText("")
        self.pages_input.clear()
        self.drop_zone.show()
        self.file_info_container.hide()
        self.options_section.setEnabled(False)
        self.actions_section.setEnabled(False)

    def extract_pages(self):
        """Extract specific pages from PDF."""
        self._hide_status()
        if not self.input_file:
            self._show_status("⚠️ Please select a PDF file to extract pages from.", "error")
            return

        page_text = self.pages_input.text().strip()
        if not page_text:
            self._show_status("⚠️ Please enter page numbers to extract.", "error")
            return

        page_numbers = parse_page_numbers(page_text)
        if page_numbers is None:
            self._show_status("❌ Invalid page numbers format. Use format like: 1,3,5-7", "error")
            return

        if not page_numbers:
            self._show_status("⚠️ No valid page numbers specified.", "error")
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Extracted Pages", "extracted.pdf", "PDF Files (*.pdf)"
        )
        if not output_file:
            return
            
        try:
            with Splitter(self.input_file) as splitter:
                splitter.extract_pages(output_file, page_numbers)
            self._show_status(f"✅ Pages extracted successfully! Saved to: {output_file}", "success")
        except Exception as e:
            self._show_status(f"❌ Failed to extract pages: {str(e)}", "error")

    def _apply_styles(self):
        """Apply futuristic styles to extract view."""
        self.setStyleSheet("""
            ExtractView {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:1 #16213e);
            }
            
            QLabel#sectionTitle {
                font-size: 32px;
                font-weight: 700;
                color: #00d9ff;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            
            QLabel#sectionSubtitle {
                font-size: 14px;
                color: #8892b0;
                letter-spacing: 1px;
            }
            
            QFrame[class="file-section"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1f3a, stop:1 #0f1729);
                border: 2px solid #00d9ff;
                border-radius: 12px;
            }
            
            QLabel[class="list-header"] {
                font-size: 13px;
                font-weight: 600;
                color: #00d9ff;
                letter-spacing: 1px;
            }
            
            QLabel#fileLabel {
                font-size: 12px;
                color: #00d9ff;
                padding: 8px;
                background: rgba(0, 217, 255, 0.1);
                border-radius: 4px;
                border: 1px solid rgba(0, 217, 255, 0.3);
            }
            
            QLabel#pageInfoLabel {
                font-size: 11px;
                color: #00d9ff;
                font-weight: 600;
            }
            
            QLabel#optionLabel {
                font-size: 11px;
                font-weight: 600;
                color: #00d9ff;
                margin-top: 4px;
            }
            
            QLineEdit {
                background: #0a0e27;
                border: 1px solid #00d9ff;
                border-radius: 6px;
                padding: 8px;
                color: #8892b0;
            }
            
            QLineEdit:focus {
                border: 2px solid #00d9ff;
            }
            
            QPushButton[class="secondary-button"] {
                background: transparent;
                color: #8892b0;
                border: 2px solid #8892b0;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 13px;
                letter-spacing: 1px;
            }
            
            QPushButton[class="secondary-button"]:hover {
                border-color: #00d9ff;
                color: #00d9ff;
            }
            
            QPushButton[class="secondary-button"]:disabled {
                border-color: #3a3f5a;
                color: #3a3f5a;
            }
            
            QPushButton[class="primary-button"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7b2cbf, stop:1 #9d4edd);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 32px;
                font-weight: 700;
                font-size: 14px;
                letter-spacing: 1px;
            }
            
            QPushButton[class="primary-button"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9d4edd, stop:1 #c77dff);
            }
            
            QPushButton[class="primary-button"]:disabled {
                background: #3a3f5a;
                color: #6c757d;
            }
            
            QWidget#statusContainer {
                background: rgba(0, 217, 255, 0.15);
                border: 1px solid #00d9ff;
                border-radius: 8px;
            }
            
            QWidget#statusContainer[statusType="error"] {
                background: rgba(255, 71, 87, 0.15);
                border: 1px solid #ff4757;
            }
            
            QWidget#statusContainer[statusType="success"] {
                background: rgba(0, 255, 127, 0.15);
                border: 1px solid #00ff7f;
            }
            
            QLabel#statusLabel {
                font-size: 13px;
                color: #00d9ff;
                background: transparent;
                border: none;
            }
            
            QWidget#statusContainer[statusType="error"] QLabel#statusLabel {
                color: #ff4757;
            }
            
            QWidget#statusContainer[statusType="success"] QLabel#statusLabel {
                color: #00ff7f;
            }
            
            QPushButton#statusCloseBtn {
                background: rgba(0, 217, 255, 0.2);
                border: 1px solid #00d9ff;
                border-radius: 4px;
                color: #00d9ff;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
            }
            
            QPushButton#statusCloseBtn:hover {
                background: rgba(0, 217, 255, 0.3);
                color: #00f0ff;
            }
            
            QWidget#statusContainer[statusType="error"] QPushButton#statusCloseBtn {
                background: rgba(255, 71, 87, 0.2);
                border-color: #ff4757;
                color: #ff4757;
            }
            
            QWidget#statusContainer[statusType="error"] QPushButton#statusCloseBtn:hover {
                background: rgba(255, 71, 87, 0.3);
                color: #ff6b7a;
            }
            
            QWidget#statusContainer[statusType="success"] QPushButton#statusCloseBtn {
                background: rgba(0, 255, 127, 0.2);
                border-color: #00ff7f;
                color: #00ff7f;
            }
            
            QWidget#statusContainer[statusType="success"] QPushButton#statusCloseBtn:hover {
                background: rgba(0, 255, 127, 0.3);
                color: #00ff9f;
            }
        """)
