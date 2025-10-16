from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QFrame, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt, QThread, Signal
from src.modules.encrypt import PDFEncryptor
from src.modules.pdf_utils import get_pdf_info
from src.ui.widgets.drop_zone import DropZone


class AddPasswordWorker(QThread):
    """Worker thread for adding password."""
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, input_file, output_file, user_password, owner_password=None):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.user_password = user_password
        self.owner_password = owner_password

    def run(self):
        try:
            with PDFEncryptor(self.input_file) as encryptor:
                result = encryptor.add_password(self.output_file, self.user_password, self.owner_password)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class AddPasswordView(QWidget):
    """Add password protection to PDF."""

    def __init__(self, on_back_click=None):
        super().__init__()
        self._on_back_click = on_back_click
        self.input_file = None
        self.total_pages = 0
        self.worker = None
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Set up the UI."""
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
        layout.setSpacing(16)

        header = self._create_header()
        layout.addWidget(header, 0)

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
        layout.addWidget(self.status_container, 0)

        file_section = self._create_file_section()
        layout.addWidget(file_section, 0)

        self.options_section = self._create_options_section()
        self.options_section.setEnabled(False)
        layout.addWidget(self.options_section, 0)

        self.actions_section = self._create_actions()
        self.actions_section.setEnabled(False)
        layout.addWidget(self.actions_section, 0)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    @staticmethod
    def _create_header():
        """Create the header section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Add Password Protection")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        subtitle = QLabel("Encrypt PDF files with password protection (AES-256)")
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
        self.file_label.setMaximumHeight(35)
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

        options_header = QLabel("PASSWORD OPTIONS")
        options_header.setProperty("class", "list-header")
        layout.addWidget(options_header)

        user_label = QLabel("User Password (required)")
        user_label.setObjectName("fieldLabel")
        layout.addWidget(user_label)

        self.user_password_input = QLineEdit()
        self.user_password_input.setPlaceholderText("Enter password to open the PDF")
        self.user_password_input.setObjectName("pagesInput")
        self.user_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.user_password_input)

        owner_label = QLabel("Owner Password (optional)")
        owner_label.setObjectName("fieldLabel")
        layout.addWidget(owner_label)

        owner_help = QLabel("💡 Owner password allows full permissions (edit, print, copy). If not set, user password will be used.")
        owner_help.setObjectName("helpLabel")
        owner_help.setWordWrap(True)
        layout.addWidget(owner_help)

        self.owner_password_input = QLineEdit()
        self.owner_password_input.setPlaceholderText("Enter owner password (leave empty to use user password)")
        self.owner_password_input.setObjectName("pagesInput")
        self.owner_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.owner_password_input)

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

        self.process_btn = QPushButton("🔒  ENCRYPT PDF")
        self.process_btn.setProperty("class", "primary-button")
        self.process_btn.clicked.connect(self.process_pdf)
        layout.addWidget(self.process_btn)

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
        self.user_password_input.clear()
        self.owner_password_input.clear()
        self.drop_zone.show()
        self.file_info_container.hide()
        self.options_section.setEnabled(False)
        self.actions_section.setEnabled(False)

    def process_pdf(self):
        """Process PDF encryption."""
        self._hide_status()
        if not self.input_file:
            self._show_status("⚠️ Please select a PDF file.", "error")
            return

        user_password = self.user_password_input.text().strip()
        if not user_password:
            self._show_status("⚠️ Please enter a user password.", "error")
            return

        owner_password = self.owner_password_input.text().strip() or None

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Encrypted PDF", "encrypted.pdf", "PDF Files (*.pdf)"
        )
        if not output_file:
            return

        self.process_btn.setText("⏳ Processing...")
        self.process_btn.setEnabled(False)
        self.options_section.setEnabled(False)

        self.worker = AddPasswordWorker(self.input_file, output_file, user_password, owner_password)
        self.worker.finished.connect(self._on_process_complete)
        self.worker.error.connect(self._on_process_error)
        self.worker.start()

    def _on_process_complete(self, result):
        """Handle successful processing."""
        self._show_status(f"✅ PDF encrypted successfully! {result['page_count']} pages processed.", "success")
        self.process_btn.setText("🔒  ENCRYPT PDF")
        self.process_btn.setEnabled(True)
        self.options_section.setEnabled(True)

    def _on_process_error(self, error_msg):
        """Handle processing error."""
        self._show_status(f"❌ Failed: {error_msg}", "error")
        self.process_btn.setText("🔒  ENCRYPT PDF")
        self.process_btn.setEnabled(True)
        self.options_section.setEnabled(True)

    def _apply_styles(self):
        """Apply styles."""
        self.setStyleSheet("""
            AddPasswordView {
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
            
            QLabel#fieldLabel {
                font-size: 12px;
                color: #00d9ff;
                font-weight: 600;
                margin-top: 8px;
            }
            
            QLabel#helpLabel {
                font-size: 11px;
                color: #8892b0;
                padding: 8px;
                background: rgba(0, 217, 255, 0.05);
                border-radius: 4px;
                border-left: 3px solid #00d9ff;
            }
            
            QLabel#fileLabel {
                font-size: 12px;
                color: #00d9ff;
                padding: 6px 8px;
                background: rgba(0, 217, 255, 0.1);
                border-radius: 4px;
                border: 1px solid rgba(0, 217, 255, 0.3);
            }
            
            QLabel#pageInfoLabel {
                font-size: 11px;
                color: #00d9ff;
                font-weight: 600;
            }
            
            QLineEdit#pagesInput {
                background: #0a0e27;
                border: 1px solid #00d9ff;
                border-radius: 6px;
                padding: 8px;
                color: #8892b0;
            }
            
            QLineEdit#pagesInput:focus {
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
