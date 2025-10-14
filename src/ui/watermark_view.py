from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QLineEdit, QSlider, QFrame
import os

from src.ui.widgets.drop_zone import DropZone
from src.modules.watermark import Watermarker


class WatermarkWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, input_path, output_path, text, opacity):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.text = text
        self.opacity = opacity
    
    def run(self):
        try:
            with Watermarker(self.input_path) as watermarker:
                result = watermarker.add_watermark(self.output_path, self.text, self.opacity)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class WatermarkView(QWidget):
    """View for adding watermarks to PDF."""

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

        header = QLabel("ADD WATERMARK")
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
        
        text_label = QLabel("Watermark text:")
        options_layout.addWidget(text_label)
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter watermark text...")
        self.text_input.setMaxLength(50)
        options_layout.addWidget(self.text_input)
        
        opacity_label = QLabel("Opacity:")
        options_layout.addWidget(opacity_label)
        
        opacity_container = QHBoxLayout()
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(10)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(30)
        self.opacity_slider.valueChanged.connect(self._update_opacity_label)
        opacity_container.addWidget(self.opacity_slider)
        
        self.opacity_value_label = QLabel("30%")
        self.opacity_value_label.setFixedWidth(50)
        opacity_container.addWidget(self.opacity_value_label)
        options_layout.addLayout(opacity_container)
        
        self.options_section = options_section
        self.options_section.setEnabled(False)
        layout.addWidget(options_section)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self._clear_file)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()

        self.watermark_btn = QPushButton("💧  Add Watermark")
        self.watermark_btn.setObjectName("primaryButton")
        self.watermark_btn.setEnabled(False)
        self.watermark_btn.clicked.connect(self._add_watermark)
        button_layout.addWidget(self.watermark_btn)
        
        self.worker = None

        layout.addLayout(button_layout)

    def _update_opacity_label(self, value):
        self.opacity_value_label.setText(f"{value}%")

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
        self.options_section.setEnabled(True)
        self.watermark_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self._hide_status()

    def _clear_file(self):
        self.current_file = None
        self.file_info.setVisible(False)
        self.options_section.setEnabled(False)
        self.watermark_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

    def _add_watermark(self):
        if not self.current_file or self.worker:
            return
        
        text = self.text_input.text().strip()
        if not text:
            self._show_status("⚠️ Please enter watermark text.", "error")
            return

        base_name = os.path.splitext(os.path.basename(self.current_file))[0]
        default_name = f"{base_name}_watermarked.pdf"
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Watermarked PDF", default_name, "PDF Files (*.pdf)"
        )

        if not output_path:
            output_path = default_name

        self.output_path = output_path
        opacity = self.opacity_slider.value() / 100.0
        
        self.watermark_btn.setText("⏳ Adding Watermark...")
        self.watermark_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.options_section.setEnabled(False)
        
        self.worker = WatermarkWorker(self.current_file, output_path, text, opacity)
        self.worker.finished.connect(self._on_watermark_finished)
        self.worker.error.connect(self._on_watermark_error)
        self.worker.start()
    
    def _on_watermark_finished(self, result):
        output_mb = result["output_size"] / (1024 * 1024)
        page_count = result["page_count"]
        message = f"✅ Watermark added to {page_count} page(s)! Size: {output_mb:.2f} MB\nSaved to: {self.output_path}"
        
        self.watermark_btn.setText("💧  Add Watermark")
        self.watermark_btn.setEnabled(True)
        self.options_section.setEnabled(True)
        self.worker = None
        
        self._show_status(message, "success")
        self._clear_file()
    
    def _on_watermark_error(self, error_msg):
        self.watermark_btn.setText("💧  Add Watermark")
        self.watermark_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.options_section.setEnabled(True)
        self.worker = None
        
        self._show_status(f"❌ Failed to add watermark: {error_msg}", "error")

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
            WatermarkView {
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
            
            QSlider::groove:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1f3a, stop:1 #0f1729);
                height: 8px;
                border-radius: 4px;
                border: 1px solid rgba(0, 217, 255, 0.3);
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #00b8d4);
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
                border: 2px solid #00d9ff;
            }
            
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00f0ff, stop:1 #00d9ff);
                border-color: #00f0ff;
            }
            
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #7b2cbf);
                border-radius: 4px;
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
