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
    QMessageBox,
)
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
        layout.addWidget(self.file_list)

        add_btn = QPushButton("📁  Add PDF Files")
        add_btn.setProperty("class", "add-button")
        add_btn.clicked.connect(self.add_files)
        layout.addWidget(add_btn)

        return container

    def _create_actions(self):
        """Create the action buttons section."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(16)

        clear_btn = QPushButton("Clear All")
        clear_btn.setProperty("class", "secondary-button")
        clear_btn.clicked.connect(self.clear_files)
        layout.addWidget(clear_btn)

        layout.addStretch()

        merge_btn = QPushButton("🔗  Merge PDFs")
        merge_btn.setProperty("class", "primary-button")
        merge_btn.clicked.connect(self.merge_files)
        layout.addWidget(merge_btn)

        return container

    def add_files(self):
        """Add PDF files to the list."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        if files:
            for file_path in files:
                if file_path not in self.files:
                    self.files.append(file_path)
                    item = QListWidgetItem(os.path.basename(file_path))
                    item.setToolTip(file_path)
                    self.file_list.addItem(item)

    def clear_files(self):
        """Clear all files from the list."""
        self.files.clear()
        self.file_list.clear()

    def merge_files(self):
        """Merge the selected PDF files."""
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please add PDF files to merge.")
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "merged.pdf", "PDF Files (*.pdf)"
        )
        if output_file:
            try:
                with Merger() as merger:
                    merger.process(self.files, output_file)
                QMessageBox.information(
                    self,
                    "Success",
                    f"PDFs merged successfully!\nSaved to: {output_file}",
                )
                self.clear_files()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to merge PDFs:\n{str(e)}")

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
        """)
