from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QListWidget,
    QLabel,
    QFrame,
    QListWidgetItem,
)
from PySide6.QtCore import Qt
from src.modules.merge import Merger
from src.ui.widgets.drop_zone import DropZone


class MergeView(QWidget):
    """Futuristic merge view."""

    def __init__(self, on_back_click=None):
        super().__init__()
        self._on_back_click = on_back_click
        self.files = []
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Set up the merge view UI."""
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
        layout.addWidget(file_section, 1)

        # Actions
        actions = self._create_actions()
        layout.addWidget(actions)

    @staticmethod
    def _create_header():
        """Create the header section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Merge PDF Files")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        subtitle = QLabel("Select PDF files to combine into a single document")
        subtitle.setObjectName("sectionSubtitle")
        layout.addWidget(subtitle)

        return container

    def _create_file_section(self):
        """Create the file list section."""
        container = QFrame()
        container.setProperty("class", "file-section")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Drop zone
        drop_zone = DropZone()
        drop_zone.filesDropped.connect(self._handle_dropped_files)
        layout.addWidget(drop_zone)

        list_header = QLabel("SELECTED FILES")
        list_header.setProperty("class", "list-header")
        layout.addWidget(list_header)

        self.file_list = QListWidget()
        self.file_list.setProperty("class", "file-list")
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self._show_context_menu)
        self.file_list.itemSelectionChanged.connect(self._update_remove_button_state)
        layout.addWidget(self.file_list, 1)

        return container

    def _create_actions(self):
        """Create the action buttons section."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(16)

        self.remove_btn = QPushButton("REMOVE")
        self.remove_btn.setProperty("class", "secondary-button")
        self.remove_btn.clicked.connect(self.remove_selected_file)
        self.remove_btn.setEnabled(False)
        layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("CLEAR ALL")
        self.clear_btn.setProperty("class", "secondary-button")
        self.clear_btn.clicked.connect(self.clear_files)
        self.clear_btn.setEnabled(False)
        layout.addWidget(self.clear_btn)

        layout.addStretch()

        self.merge_btn = QPushButton("🔗  MERGE PDFs")
        self.merge_btn.setProperty("class", "primary-button")
        self.merge_btn.clicked.connect(self.merge_files)
        self.merge_btn.setEnabled(False)
        layout.addWidget(self.merge_btn)

        return container

    def _update_remove_button_state(self):
        """Enable/disable remove button based on selection."""
        self.remove_btn.setEnabled(self.file_list.currentRow() >= 0)

    def _update_button_states(self):
        """Update all button states based on file count."""
        has_files = len(self.files) > 0
        self.clear_btn.setEnabled(has_files)
        self.merge_btn.setEnabled(len(self.files) >= 2)

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

    def _handle_dropped_files(self, files):
        """Handle files dropped into drop zone."""
        self._hide_status()
        if not files:
            self.add_files()
            return
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
                item = QListWidgetItem(file_path)
                self.file_list.addItem(item)
        self._update_button_states()

    def add_files(self):
        """Add PDF files to the list."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        if files:
            self._handle_dropped_files(files)

    def remove_selected_file(self):
        """Remove the selected file from the list."""
        self._hide_status()
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            self.file_list.takeItem(current_row)
            del self.files[current_row]
            self._update_button_states()

    def _show_context_menu(self, position):
        """Show context menu for file list."""
        if self.file_list.itemAt(position):
            from PySide6.QtWidgets import QMenu
            menu = QMenu()
            remove_action = menu.addAction("Remove")
            action = menu.exec(self.file_list.mapToGlobal(position))
            if action == remove_action:
                self.remove_selected_file()

    def clear_files(self):
        """Clear all files from the list."""
        self._hide_status()
        self.files.clear()
        self.file_list.clear()
        self._update_button_states()

    def merge_files(self):
        """Merge the selected PDF files."""
        self._hide_status()
        if len(self.files) < 2:
            self._show_status("⚠️ Please add at least 2 PDF files to merge.", "error")
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "merged.pdf", "PDF Files (*.pdf)"
        )
        if not output_file:
            return
        
        self.merge_btn.setText("⏳ Merging...")
        self.merge_btn.setEnabled(False)
        self.remove_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
            
        try:
            with Merger() as merger:
                merger.process(self.files, output_file)
            self._show_status(f"✅ PDFs merged successfully! Saved to: {output_file}", "success")
        except Exception as e:
            self._show_status(f"❌ Failed to merge PDFs: {str(e)}", "error")
        finally:
            self.merge_btn.setText("🔗  MERGE PDFs")
            self.merge_btn.setEnabled(True)
            self.remove_btn.setEnabled(self.file_list.currentRow() >= 0)
            self.clear_btn.setEnabled(True)

    def _apply_styles(self):
        """Apply futuristic styles to merge view."""
        self.setStyleSheet("""
            MergeView {
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
            
            QListWidget[class="file-list"] {
                background: #0a0e27;
                border: 1px solid #00d9ff;
                border-radius: 8px;
                color: #8892b0;
                padding: 8px;
            }
            
            QListWidget[class="file-list"]::item {
                padding: 8px;
                border-radius: 4px;
            }
            
            QListWidget[class="file-list"]::item:selected {
                background: rgba(0, 217, 255, 0.2);
                color: #00d9ff;
            }
            
            QListWidget[class="file-list"]::item:hover {
                background: rgba(0, 217, 255, 0.1);
            }
            
            QPushButton[class="add-button"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #00b8d4);
                color: #0a0e27;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 13px;
                letter-spacing: 1px;
            }
            
            QPushButton[class="add-button"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00f0ff, stop:1 #00d9ff);
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
