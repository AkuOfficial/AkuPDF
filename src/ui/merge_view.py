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
from PySide6.QtCore import Qt, QTimer
from src.modules.merge import Merger
import os


class MergeView(QWidget):
    """Material Design merge view."""

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
        layout.setSpacing(32)

        # Header
        header = self._create_header()
        layout.addWidget(header)

        # Status message
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        layout.addWidget(self.status_label)

        # File section
        file_section = self._create_file_section()
        layout.addWidget(file_section, 1)

        # Actions
        actions = self._create_actions()
        layout.addWidget(actions)

    def _create_header(self):
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

        list_header = QLabel("Selected Files")
        list_header.setProperty("class", "list-header")
        layout.addWidget(list_header)

        self.file_list = QListWidget()
        self.file_list.setProperty("class", "file-list")
        self.file_list.setMinimumHeight(300)
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self._show_context_menu)
        self.file_list.itemSelectionChanged.connect(self._update_remove_button_state)
        layout.addWidget(self.file_list)

        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("📁  Add PDF Files")
        add_btn.setProperty("class", "add-button")
        add_btn.clicked.connect(self.add_files)
        buttons_layout.addWidget(add_btn)

        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.setProperty("class", "secondary-button")
        self.remove_btn.clicked.connect(self.remove_selected_file)
        self.remove_btn.setEnabled(False)
        buttons_layout.addWidget(self.remove_btn)

        layout.addLayout(buttons_layout)

        return container

    def _create_actions(self):
        """Create the action buttons section."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(16)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setProperty("class", "secondary-button")
        self.clear_btn.clicked.connect(self.clear_files)
        self.clear_btn.setEnabled(False)
        layout.addWidget(self.clear_btn)

        layout.addStretch()

        self.merge_btn = QPushButton("🔗  Merge PDFs")
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

    def _show_status(self, message, is_error=False):
        """Show status message inline."""
        self.status_label.setText(message)
        self.status_label.setProperty("error", is_error)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.show()
        
        # Auto-hide after 5 seconds
        QTimer.singleShot(5000, self.status_label.hide)

    def add_files(self):
        """Add PDF files to the list."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        if files:
            for file_path in files:
                if file_path not in self.files:
                    self.files.append(file_path)
                    item = QListWidgetItem(file_path)
                    self.file_list.addItem(item)
            self._update_button_states()

    def remove_selected_file(self):
        """Remove the selected file from the list."""
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
        self.files.clear()
        self.file_list.clear()
        self._update_button_states()

    def merge_files(self):
        """Merge the selected PDF files."""
        if len(self.files) < 2:
            self._show_status("⚠️ Please add at least 2 PDF files to merge.", True)
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "merged.pdf", "PDF Files (*.pdf)"
        )
        if output_file:
            try:
                with Merger() as merger:
                    merger.process(self.files, output_file)
                self._show_status(f"✅ PDFs merged successfully! Saved to: {output_file}")
                self.clear_files()
            except Exception as e:
                self._show_status(f"❌ Failed to merge PDFs: {str(e)}", True)

    def _apply_styles(self):
        """Apply styles to merge view."""
        self.setStyleSheet("""
            MergeView {
                background: #f8f9fa;
            }
            
            QLabel#sectionTitle {
                font-size: 32px;
                font-weight: 700;
                color: #212529;
            }
            
            QLabel#sectionSubtitle {
                font-size: 16px;
                color: #6c757d;
            }
            
            QLabel#statusLabel {
                font-size: 14px;
                padding: 12px 16px;
                border-radius: 8px;
                background: #d1e7dd;
                color: #0f5132;
                border: 1px solid #badbcc;
            }
            
            QLabel#statusLabel[error="true"] {
                background: #f8d7da;
                color: #842029;
                border: 1px solid #f5c2c7;
            }
        """)
