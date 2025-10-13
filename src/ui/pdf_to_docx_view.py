from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QCheckBox, QSpinBox, QRadioButton, QButtonGroup, QFrame
import os
from pypdf import PdfReader

from src.ui.widgets.drop_zone import DropZone
from src.modules.pdf_to_docx import PdfToDocxConverter


class ConvertWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, input_path, output_path, start_page, end_page, multi_page_table):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.start_page = start_page
        self.end_page = end_page
        self.multi_page_table = multi_page_table
    
    def run(self):
        try:
            with PdfToDocxConverter(self.input_path) as converter:
                result = converter.convert(self.output_path, self.start_page, self.end_page, self.multi_page_table)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class PdfToDocxView(QWidget):
    """View for converting PDF to DOCX."""

    def __init__(self, parent=None, on_back_click=None):
        super().__init__(parent)
        self._on_back_click = on_back_click
        self.current_file = None
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(16)

        header = QLabel("CONVERT TO DOCX")
        header.setObjectName("viewTitle")
        layout.addWidget(header)

        self.status_container = QWidget()
        self.status_container.setObjectName("statusContainer")
        self.status_container.setMaximumHeight(60)
        status_layout = QHBoxLayout(self.status_container)
        status_layout.setContentsMargins(12, 12, 12, 12)
        status_layout.setSpacing(8)

        self.status_label = QLabel()
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

        self.drop_zone = DropZone()
        self.drop_zone.filesDropped.connect(self._handle_files_dropped)
        layout.addWidget(self.drop_zone)

        self.file_info = QLabel("")
        self.file_info.setObjectName("fileInfo")
        self.file_info.setVisible(False)
        self.file_info.setMaximumHeight(35)
        layout.addWidget(self.file_info)
        
        options_section = QFrame()
        options_section.setProperty("class", "file-section")
        options_layout = QVBoxLayout(options_section)
        options_layout.setContentsMargins(20, 20, 20, 20)
        options_layout.setSpacing(12)
        
        options_header = QLabel("OPTIONS")
        options_header.setProperty("class", "list-header")
        options_layout.addWidget(options_header)
        
        self.page_group = QButtonGroup(self)
        
        self.all_pages_radio = QRadioButton("Convert all pages")
        self.all_pages_radio.setObjectName("pageRadio")
        self.all_pages_radio.setChecked(True)
        self.all_pages_radio.toggled.connect(self._on_page_option_changed)
        self.page_group.addButton(self.all_pages_radio)
        options_layout.addWidget(self.all_pages_radio)
        
        self.range_radio = QRadioButton("Convert page range:")
        self.range_radio.setObjectName("pageRadio")
        self.range_radio.toggled.connect(self._on_page_option_changed)
        self.page_group.addButton(self.range_radio)
        options_layout.addWidget(self.range_radio)
        
        page_range_container = QWidget()
        page_range_layout = QHBoxLayout(page_range_container)
        page_range_layout.setContentsMargins(26, 0, 0, 0)
        page_range_layout.setSpacing(8)
        
        start_label = QLabel("Start:")
        page_range_layout.addWidget(start_label)
        self.start_page_spin = QSpinBox()
        self.start_page_spin.setMinimum(1)
        self.start_page_spin.setMaximum(9999)
        self.start_page_spin.setValue(1)
        self.start_page_spin.setEnabled(False)
        self.start_page_spin.setFixedWidth(100)
        page_range_layout.addWidget(self.start_page_spin)
        
        end_label = QLabel("End:")
        page_range_layout.addWidget(end_label)
        self.end_page_spin = QSpinBox()
        self.end_page_spin.setMinimum(1)
        self.end_page_spin.setMaximum(9999)
        self.end_page_spin.setValue(1)
        self.end_page_spin.setEnabled(False)
        self.end_page_spin.setFixedWidth(100)
        page_range_layout.addWidget(self.end_page_spin)
        page_range_layout.addStretch()
        options_layout.addWidget(page_range_container)
        
        self.multi_page_table_check = QCheckBox("Parse multi-page tables")
        self.multi_page_table_check.setObjectName("layoutCheckbox")
        self.multi_page_table_check.setChecked(True)
        options_layout.addWidget(self.multi_page_table_check)
        
        self.options_section = options_section
        self.options_section.setEnabled(False)
        layout.addWidget(options_section)
        
        self.start_page_spin.valueChanged.connect(self._validate_page_range)
        self.end_page_spin.valueChanged.connect(self._validate_page_range)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self._clear_file)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()

        self.convert_btn = QPushButton("📄  Convert to DOCX")
        self.convert_btn.setObjectName("primaryButton")
        self.convert_btn.setEnabled(False)
        self.convert_btn.clicked.connect(self._convert_pdf)
        button_layout.addWidget(self.convert_btn)
        
        self.worker = None

        layout.addLayout(button_layout)

    def _handle_files_dropped(self, files):
        if not files:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
            if file_path:
                self._on_file_selected(file_path)
        elif len(files) == 1:
            self._on_file_selected(files[0])
    
    def _on_file_selected(self, file_path):
        self.current_file = file_path
        reader = PdfReader(file_path)
        self.total_pages = len(reader.pages)
        self.file_info.setText(f"Selected: {file_path} ({self.total_pages} pages)")
        self.file_info.setVisible(True)
        self.start_page_spin.setMaximum(self.total_pages)
        self.end_page_spin.setMaximum(self.total_pages)
        self.end_page_spin.setValue(self.total_pages)
        self.options_section.setEnabled(True)
        self.convert_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self._hide_status()
    
    def _validate_page_range(self):
        if self.start_page_spin.value() > self.end_page_spin.value():
            self.end_page_spin.setValue(self.start_page_spin.value())
    
    def _on_page_option_changed(self):
        enabled = self.range_radio.isChecked()
        self.start_page_spin.setEnabled(enabled)
        self.end_page_spin.setEnabled(enabled)

    def _clear_file(self):
        self.current_file = None
        self.file_info.setVisible(False)
        self.options_section.setEnabled(False)
        self.convert_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

    def _convert_pdf(self):
        if not self.current_file or self.worker:
            return

        base_name = os.path.splitext(os.path.basename(self.current_file))[0]
        default_name = f"{base_name}.docx"
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save DOCX File", default_name, "Word Documents (*.docx)"
        )

        if not output_path:
            output_path = default_name

        self.output_path = output_path
        
        if self.all_pages_radio.isChecked():
            start_page = 0
            end_page = None
        else:
            start_page = self.start_page_spin.value() - 1
            end_page = self.end_page_spin.value()
        
        multi_page_table = self.multi_page_table_check.isChecked()
        
        self.convert_btn.setText("⏳ Converting...")
        self.convert_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.all_pages_radio.setEnabled(False)
        self.range_radio.setEnabled(False)
        self.start_page_spin.setEnabled(False)
        self.end_page_spin.setEnabled(False)
        self.multi_page_table_check.setEnabled(False)
        
        self.worker = ConvertWorker(self.current_file, output_path, start_page, end_page, multi_page_table)
        self.worker.finished.connect(self._on_convert_finished)
        self.worker.error.connect(self._on_convert_error)
        self.worker.start()
    
    def _on_convert_finished(self, result):
        output_mb = result["output_size"] / (1024 * 1024)
        message = f"✅ PDF converted to DOCX successfully! Size: {output_mb:.2f} MB\nSaved to: {self.output_path}"
        
        self.convert_btn.setText("📄  Convert to DOCX")
        self.convert_btn.setEnabled(True)
        self.all_pages_radio.setEnabled(True)
        self.range_radio.setEnabled(True)
        self._on_page_option_changed()
        self.multi_page_table_check.setEnabled(True)
        self.worker = None
        
        self._show_status(message, "success")
        self._clear_file()
    
    def _on_convert_error(self, error_msg):
        self.convert_btn.setText("📄  Convert to DOCX")
        self.convert_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.all_pages_radio.setEnabled(True)
        self.range_radio.setEnabled(True)
        self._on_page_option_changed()
        self.multi_page_table_check.setEnabled(True)
        self.worker = None
        
        self._show_status(f"❌ Failed to convert PDF: {error_msg}", "error")

    def _show_status(self, message, status_type="info"):
        self.status_label.setText(message)
        self.status_container.setProperty("statusType", status_type)
        self.status_container.style().unpolish(self.status_container)
        self.status_container.style().polish(self.status_container)
        self.status_container.show()

    def _hide_status(self):
        self.status_container.hide()

    def _apply_styles(self):
        self.setStyleSheet("""
            PdfToDocxView {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:1 #16213e);
            }
            
            QLabel#viewTitle {
                font-size: 32px;
                font-weight: 700;
                color: #00d9ff;
                letter-spacing: 3px;
            }
            
            QLabel#fileInfo {
                font-size: 11px;
                color: #8892b0;
                padding: 6px 8px;
                background: rgba(0, 217, 255, 0.05);
                border: 1px solid rgba(0, 217, 255, 0.2);
                border-radius: 4px;
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
            
            QLabel#optionLabel {
                font-size: 13px;
                color: #8892b0;
                font-weight: 600;
            }
            
            QSpinBox#optionSpin {
                background: rgba(26, 31, 58, 0.8);
                color: #00d9ff;
                border: 1px solid rgba(0, 217, 255, 0.3);
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                min-width: 80px;
            }
            
            QSpinBox#optionSpin:hover {
                border-color: #00d9ff;
            }
            
            QCheckBox#optionCheck {
                color: #8892b0;
                font-size: 13px;
                spacing: 8px;
            }
            
            QCheckBox#optionCheck::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #00d9ff;
                border-radius: 4px;
                background: #0a0e27;
            }
            
            QCheckBox#optionCheck::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #00b8d4);
            }
            
            QCheckBox#optionCheck::indicator:hover {
                border-color: #00f0ff;
            }
            
            QRadioButton#optionRadio {
                color: #8892b0;
                font-size: 13px;
                spacing: 8px;
            }
            
            QRadioButton#optionRadio::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #00d9ff;
                border-radius: 9px;
                background: #0a0e27;
            }
            
            QRadioButton#optionRadio::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #00b8d4);
            }
            
            QRadioButton#optionRadio::indicator:hover {
                border-color: #00f0ff;
            }
            
            QPushButton#primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #7b2cbf);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 28px;
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 1px;
            }
            
            QPushButton#primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00f0ff, stop:1 #9d4edd);
            }
            
            QPushButton#primaryButton:disabled {
                background: #2a2f4a;
                color: #5a5f7a;
            }
            
            QPushButton#secondaryButton {
                background: rgba(136, 146, 176, 0.1);
                color: #8892b0;
                border: 1px solid rgba(136, 146, 176, 0.3);
                border-radius: 8px;
                padding: 14px 28px;
                font-size: 14px;
                font-weight: 500;
            }
            
            QPushButton#secondaryButton:hover {
                background: rgba(136, 146, 176, 0.2);
                color: #00d9ff;
                border-color: #00d9ff;
            }
            
            QWidget#statusContainer {
                background: rgba(0, 217, 255, 0.15);
                border: 1px solid #00d9ff;
                border-radius: 8px;
                min-height: 50px;
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
