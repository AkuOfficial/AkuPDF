from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QComboBox, QSpinBox, QGroupBox
import os

from src.ui.widgets.drop_zone import DropZone
from src.modules.pdf_to_images import PdfToImagesConverter


class ConvertWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, input_path, output_folder, image_format, dpi):
        super().__init__()
        self.input_path = input_path
        self.output_folder = output_folder
        self.image_format = image_format
        self.dpi = dpi
    
    def run(self):
        try:
            with PdfToImagesConverter(self.input_path) as converter:
                result = converter.convert(self.output_folder, self.image_format, self.dpi)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class PdfToImagesView(QWidget):
    """View for converting PDF to images."""

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

        header = QLabel("CONVERT TO IMAGES")
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

        options_group = QGroupBox("Options")
        options_group.setObjectName("optionsGroup")
        options_layout = QVBoxLayout()
        
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["png", "jpg", "jpeg"])
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        options_layout.addLayout(format_layout)
        
        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(QLabel("DPI:"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setMinimum(72)
        self.dpi_spin.setMaximum(600)
        self.dpi_spin.setValue(150)
        self.dpi_spin.setSingleStep(50)
        dpi_layout.addWidget(self.dpi_spin)
        dpi_layout.addStretch()
        options_layout.addLayout(dpi_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self._clear_file)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()

        self.convert_btn = QPushButton("🖼️  Convert to Images")
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
        self.file_info.setText(f"Selected: {file_path}")
        self.file_info.setVisible(True)
        self.convert_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self._hide_status()

    def _clear_file(self):
        self.current_file = None
        self.file_info.setVisible(False)
        self.convert_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

    def _convert_pdf(self):
        if not self.current_file or self.worker:
            return

        base_name = os.path.splitext(os.path.basename(self.current_file))[0]
        default_folder = f"{base_name}_images"
        
        output_folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder", default_folder
        )

        if not output_folder:
            output_folder = default_folder

        self.output_folder = output_folder
        
        image_format = self.format_combo.currentText()
        dpi = self.dpi_spin.value()
        
        self.convert_btn.setText("⏳ Converting...")
        self.convert_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        
        self.worker = ConvertWorker(self.current_file, output_folder, image_format, dpi)
        self.worker.finished.connect(self._on_convert_finished)
        self.worker.error.connect(self._on_convert_error)
        self.worker.start()
    
    def _on_convert_finished(self, result):
        total_mb = result["total_size"] / (1024 * 1024)
        page_count = result["page_count"]
        message = f"✅ PDF converted to {page_count} image(s)! Total size: {total_mb:.2f} MB\nSaved to: {self.output_folder}"
        
        self.convert_btn.setText("🖼️  Convert to Images")
        self.convert_btn.setEnabled(True)
        self.worker = None
        
        self._show_status(message, "success")
        self._clear_file()
    
    def _on_convert_error(self, error_msg):
        self.convert_btn.setText("🖼️  Convert to Images")
        self.convert_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
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
            PdfToImagesView {
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
            
            QGroupBox#optionsGroup {
                font-size: 13px;
                font-weight: 600;
                color: #00d9ff;
                border: 1px solid rgba(0, 217, 255, 0.3);
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            
            QGroupBox#optionsGroup::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                left: 12px;
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
