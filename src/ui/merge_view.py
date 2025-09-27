from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                                QFileDialog, QListWidget, QLabel, QFrame, 
                                QListWidgetItem, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from src.modules.merge import Merger
import os


class MergeView(QWidget):
    """Modern merge view with drag-and-drop support and better UX."""
    
    def __init__(self, on_back_click=None):
        super().__init__()
        self._on_back_click = on_back_click
        self.files = []
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Set up the modern merge view UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(32)

        # Header section
        header = self._create_header()
        layout.addWidget(header)

        # File list section
        file_section = self._create_file_section()
        layout.addWidget(file_section, 1)

        # Action buttons
        actions = self._create_actions()
        layout.addWidget(actions)

    def _create_header(self):
        """Create the header section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

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
        container.setObjectName("fileSection")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # File list header
        list_header = QLabel("Selected Files")
        list_header.setObjectName("listHeader")
        layout.addWidget(list_header)

        # File list
        self.file_list = QListWidget()
        self.file_list.setObjectName("fileList")
        self.file_list.setMinimumHeight(300)
        layout.addWidget(self.file_list)

        # Add files button
        add_btn = QPushButton("📁  Add PDF Files")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.add_files)
        layout.addWidget(add_btn)

        return container

    def _create_actions(self):
        """Create the action buttons section."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(16)

        # Clear button
        clear_btn = QPushButton("Clear All")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.clicked.connect(self.clear_files)
        layout.addWidget(clear_btn)

        layout.addStretch()

        # Merge button
        merge_btn = QPushButton("🔗  Merge PDFs")
        merge_btn.setObjectName("primaryButton")
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
                    self, "Success", 
                    f"PDFs merged successfully!\nSaved to: {output_file}"
                )
                self.clear_files()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Failed to merge PDFs:\n{str(e)}"
                )

    def _apply_styles(self):
        """Apply modern styles to the merge view."""
        self.setStyleSheet("""
            MergeView {
                background: #f8f9fa;
            }
            
            #sectionTitle {
                font-size: 28px;
                font-weight: 700;
                color: #212529;
                margin: 0;
            }
            
            #sectionSubtitle {
                font-size: 16px;
                color: #6c757d;
                margin: 0;
            }
            
            #fileSection {
                background: white;
                border-radius: 16px;
                border: 1px solid #e9ecef;
            }
            
            #listHeader {
                font-size: 18px;
                font-weight: 600;
                color: #495057;
                margin: 0;
            }
            
            #fileList {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background: #f8f9fa;
                padding: 8px;
                font-size: 14px;
            }
            
            #fileList::item {
                padding: 12px;
                border-radius: 6px;
                margin: 2px 0;
            }
            
            #fileList::item:selected {
                background: #e3f2fd;
                color: #1976d2;
            }
            
            #addButton {
                background: #f8f9fa;
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                font-weight: 500;
                color: #6c757d;
            }
            
            #addButton:hover {
                background: #e9ecef;
                border-color: #007bff;
                color: #007bff;
            }
            
            #primaryButton {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            
            #primaryButton:hover {
                background: #0056b3;
            }
            
            #secondaryButton {
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            
            #secondaryButton:hover {
                background: #545b62;
            }
        """)
