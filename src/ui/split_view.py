from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QFrame, QSpinBox, QMessageBox
)
from src.modules.split import Splitter
import os


class SplitView(QWidget):
    """Split PDF view."""

    def __init__(self, on_back_click=None):
        super().__init__()
        self._on_back_click = on_back_click
        self.input_file = None
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Set up the split view UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(32)

        # Header
        header = self._create_header()
        layout.addWidget(header)

        # File section
        file_section = self._create_file_section()
        layout.addWidget(file_section)

        # Options section
        options_section = self._create_options_section()
        layout.addWidget(options_section)

        # Actions
        actions = self._create_actions()
        layout.addWidget(actions)

        layout.addStretch()

    def _create_header(self):
        """Create the header section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Split PDF Files")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        subtitle = QLabel("Split a PDF into multiple files or extract specific pages")
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

        list_header = QLabel("Input File")
        list_header.setProperty("class", "list-header")
        layout.addWidget(list_header)

        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileLabel")
        layout.addWidget(self.file_label)

        select_btn = QPushButton("📁  Select PDF File")
        select_btn.setProperty("class", "add-button")
        select_btn.clicked.connect(self.select_file)
        layout.addWidget(select_btn)

        return container

    def _create_options_section(self):
        """Create the options section."""
        container = QFrame()
        container.setProperty("class", "file-section")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        options_header = QLabel("Split Options")
        options_header.setProperty("class", "list-header")
        layout.addWidget(options_header)

        # Pages per file option
        pages_layout = QHBoxLayout()
        pages_layout.addWidget(QLabel("Pages per file:"))
        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setMinimum(1)
        self.pages_spinbox.setMaximum(100)
        self.pages_spinbox.setValue(1)
        pages_layout.addWidget(self.pages_spinbox)
        pages_layout.addStretch()
        layout.addLayout(pages_layout)

        return container

    def _create_actions(self):
        """Create the action buttons section."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(16)

        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("class", "secondary-button")
        clear_btn.clicked.connect(self.clear_file)
        layout.addWidget(clear_btn)

        layout.addStretch()

        split_btn = QPushButton("✂️  Split PDF")
        split_btn.setProperty("class", "primary-button")
        split_btn.clicked.connect(self.split_file)
        layout.addWidget(split_btn)

        return container

    def select_file(self):
        """Select input PDF file."""
        file, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file:
            self.input_file = file
            self.file_label.setText(os.path.basename(file))

    def clear_file(self):
        """Clear selected file."""
        self.input_file = None
        self.file_label.setText("No file selected")

    def split_file(self):
        """Split the PDF file."""
        if not self.input_file:
            QMessageBox.warning(self, "No File", "Please select a PDF file to split.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            try:
                with Splitter(self.input_file) as splitter:
                    pages_per_file = self.pages_spinbox.value()
                    file_count = splitter.split_by_pages(output_dir, pages_per_file)
                QMessageBox.information(
                    self, "Success",
                    f"PDF split successfully!\nCreated {file_count} files in: {output_dir}"
                )
                self.clear_file()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to split PDF:\n{str(e)}")

    def _apply_styles(self):
        """Apply styles to split view."""
        self.setStyleSheet("""
            SplitView {
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
            
            QLabel#fileLabel {
                font-size: 14px;
                color: #495057;
                padding: 8px;
                background: #f8f9fa;
                border-radius: 4px;
            }
        """)
