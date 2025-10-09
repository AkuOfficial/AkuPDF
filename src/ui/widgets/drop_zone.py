from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class DropZone(QFrame):
    """Futuristic drag-and-drop zone for PDF files."""
    
    filesDropped = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Set up the drop zone UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon
        icon_label = QLabel("📁")
        icon_label.setObjectName("dropIcon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Main text
        main_label = QLabel("DROP FILES HERE")
        main_label.setObjectName("dropMainText")
        main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(main_label)
        
        # Subtitle
        sub_label = QLabel("or click to browse")
        sub_label.setObjectName("dropSubText")
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub_label)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith('.pdf') for url in urls):
                event.acceptProposedAction()
                self.setProperty("dragActive", True)
                self.style().unpolish(self)
                self.style().polish(self)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.pdf'):
                files.append(file_path)
        
        if files:
            self.filesDropped.emit(files)
        
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        event.acceptProposedAction()
    
    def mousePressEvent(self, event):
        """Handle mouse press to trigger file dialog."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.filesDropped.emit([])  # Empty list signals to open file dialog
    
    def _apply_styles(self):
        """Apply futuristic styles."""
        self.setStyleSheet("""
            DropZone {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 217, 255, 0.05), stop:1 rgba(123, 44, 191, 0.05));
                border: 2px dashed rgba(0, 217, 255, 0.3);
                border-radius: 12px;
                min-height: 100px;
            }
            
            DropZone:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 217, 255, 0.1), stop:1 rgba(123, 44, 191, 0.1));
                border-color: rgba(0, 217, 255, 0.6);
            }
            
            DropZone[dragActive="true"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 217, 255, 0.2), stop:1 rgba(123, 44, 191, 0.2));
                border-color: #00d9ff;
                border-width: 3px;
            }
            
            QLabel#dropIcon {
                font-size: 32px;
                color: #00d9ff;
            }
            
            QLabel#dropMainText {
                font-size: 13px;
                font-weight: 700;
                color: #00d9ff;
                letter-spacing: 1px;
            }
            
            QLabel#dropSubText {
                font-size: 10px;
                color: #8892b0;
                letter-spacing: 1px;
            }
        """)
