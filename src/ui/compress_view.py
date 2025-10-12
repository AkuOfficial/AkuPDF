from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QScrollArea, QComboBox
import os

from src.ui.widgets.drop_zone import DropZone
from src.modules.compress import Compressor


class CompressWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    progress = Signal(int, int)
    
    def __init__(self, input_path, output_path, level):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.level = level
    
    def run(self):
        try:
            with Compressor(self.input_path) as compressor:
                stats = compressor.compress(
                    self.output_path, 
                    self.level,
                    progress_callback=lambda current, total: self.progress.emit(current, total)
                )
            self.finished.emit(stats)
        except Exception as e:
            self.error.emit(str(e))


class CompressView(QWidget):
    """View for compressing PDF files."""

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

        header = QLabel("COMPRESS PDF")
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
        
        level_container = QWidget()
        level_layout = QHBoxLayout(level_container)
        level_layout.setContentsMargins(0, 0, 0, 0)
        
        level_label = QLabel("Compression Level:")
        level_label.setObjectName("levelLabel")
        level_layout.addWidget(level_label)
        
        self.level_combo = QComboBox()
        self.level_combo.setObjectName("levelCombo")
        self.level_combo.addItems(["Low", "Medium", "High"])
        self.level_combo.setCurrentIndex(1)
        level_layout.addWidget(self.level_combo)
        level_layout.addStretch()
        
        layout.addWidget(level_container)

        self.file_info = QLabel("")
        self.file_info.setObjectName("fileInfo")
        self.file_info.setVisible(False)
        self.file_info.setMaximumHeight(35)
        layout.addWidget(self.file_info)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self._clear_file)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()

        self.compress_btn = QPushButton("🗜️  Compress PDF")
        self.compress_btn.setObjectName("primaryButton")
        self.compress_btn.setEnabled(False)
        self.compress_btn.clicked.connect(self._compress_pdf)
        button_layout.addWidget(self.compress_btn)
        
        self.worker = None

        layout.addLayout(button_layout)

    def _handle_files_dropped(self, files):
        if not files:
            from PySide6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
            if file_path:
                self._on_file_selected(file_path)
        elif len(files) == 1:
            self._on_file_selected(files[0])
    
    def _on_file_selected(self, file_path):
        self.current_file = file_path
        self.file_info.setText(f"Selected: {file_path}")
        self.file_info.setVisible(True)
        self.compress_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self._hide_status()

    def _clear_file(self):
        self.current_file = None
        self.file_info.setVisible(False)
        self.compress_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

    def _compress_pdf(self):
        if not self.current_file or self.worker:
            return

        base_name = os.path.splitext(os.path.basename(self.current_file))[0]
        default_name = f"{base_name}_compressed.pdf"
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Compressed PDF", default_name, "PDF Files (*.pdf)"
        )

        if not output_path:
            output_path = default_name

        self.output_path = output_path
        level = self.level_combo.currentText().lower()
        
        self.compress_btn.setText("⏳ Compressing...")
        self.compress_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.level_combo.setEnabled(False)
        
        self.worker = CompressWorker(self.current_file, output_path, level)
        self.worker.finished.connect(self._on_compress_finished)
        self.worker.error.connect(self._on_compress_error)
        self.worker.start()
    
    def _on_compress_finished(self, stats):
        original_mb = stats["original_size"] / (1024 * 1024)
        compressed_mb = stats["compressed_size"] / (1024 * 1024)
        reduction = stats["reduction_percent"]

        message = f"✅ PDF compressed successfully! Original: {original_mb:.2f} MB → Compressed: {compressed_mb:.2f} MB (Reduction: {reduction:.1f}%)\nSaved to: {self.output_path}"
        
        self.compress_btn.setText("🗜️  Compress PDF")
        self.compress_btn.setEnabled(True)
        self.level_combo.setEnabled(True)
        self.worker = None
        
        self._show_status(message, "success")
        self._clear_file()
    
    def _on_compress_error(self, error_msg):
        self.compress_btn.setText("🗜️  Compress PDF")
        self.compress_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.level_combo.setEnabled(True)
        self.worker = None
        
        self._show_status(f"❌ Failed to compress PDF: {error_msg}", "error")

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
            CompressView {
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
            
            QLabel#levelLabel {
                font-size: 13px;
                color: #8892b0;
                font-weight: 600;
            }
            
            QComboBox#levelCombo {
                background: rgba(26, 31, 58, 0.8);
                color: #00d9ff;
                border: 1px solid rgba(0, 217, 255, 0.3);
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                min-width: 120px;
            }
            
            QComboBox#levelCombo:hover {
                border-color: #00d9ff;
            }
            
            QComboBox#levelCombo::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox#levelCombo QAbstractItemView {
                background: #1a1f3a;
                color: #00d9ff;
                border: 1px solid #00d9ff;
                selection-background-color: rgba(0, 217, 255, 0.2);
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
