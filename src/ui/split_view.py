from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QFrame, QSpinBox, QMessageBox, QSlider
)
from PySide6.QtCore import Qt
from src.modules.split import Splitter
import os


class SplitView(QWidget):
    """Split PDF view."""

    def __init__(self, on_back_click=None):
        super().__init__()
        self._on_back_click = on_back_click
        self.input_file = None
        self.total_pages = 0
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
        self.options_section = self._create_options_section()
        self.options_section.setEnabled(False)
        layout.addWidget(self.options_section)

        # Actions
        self.actions_section = self._create_actions()
        self.actions_section.setEnabled(False)
        layout.addWidget(self.actions_section)

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

        self.page_info_label = QLabel("")
        self.page_info_label.setObjectName("pageInfoLabel")
        layout.addWidget(self.page_info_label)

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

        # Pages per file option with slider
        pages_layout = QVBoxLayout()
        
        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel("Pages per file:"))
        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setMinimum(1)
        self.pages_spinbox.setMaximum(1)
        self.pages_spinbox.setValue(1)
        self.pages_spinbox.valueChanged.connect(self._sync_slider_from_spinbox)
        label_layout.addWidget(self.pages_spinbox)
        label_layout.addStretch()
        pages_layout.addLayout(label_layout)
        
        # Slider with min/max labels
        slider_container = QHBoxLayout()
        
        self.slider_min_label = QLabel("1")
        self.slider_min_label.setObjectName("sliderLabel")
        slider_container.addWidget(self.slider_min_label)
        
        self.pages_slider = QSlider(Qt.Orientation.Horizontal)
        self.pages_slider.setMinimum(1)
        self.pages_slider.setMaximum(1)
        self.pages_slider.setValue(1)
        self.pages_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.pages_slider.setTickInterval(1)
        self.pages_slider.valueChanged.connect(self._sync_spinbox_from_slider)
        slider_container.addWidget(self.pages_slider)
        
        self.slider_max_label = QLabel("1")
        self.slider_max_label.setObjectName("sliderLabel")
        slider_container.addWidget(self.slider_max_label)
        
        pages_layout.addLayout(slider_container)
        
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

    def _sync_slider_from_spinbox(self, value):
        """Sync slider when spinbox changes."""
        self.pages_slider.blockSignals(True)
        self.pages_slider.setValue(value)
        self.pages_slider.blockSignals(False)

    def _sync_spinbox_from_slider(self, value):
        """Sync spinbox when slider changes."""
        self.pages_spinbox.blockSignals(True)
        self.pages_spinbox.setValue(value)
        self.pages_spinbox.blockSignals(False)

    def select_file(self):
        """Select input PDF file."""
        file, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file:
            try:
                from pypdf import PdfReader
                reader = PdfReader(file, strict=False)
                self.total_pages = len(reader.pages)
                
                if self.total_pages == 0:
                    QMessageBox.warning(
                        self, "Empty PDF", 
                        "The selected PDF has no pages and cannot be split."
                    )
                    return
                
                self.input_file = file
                self.file_label.setText(os.path.basename(file))
                self.page_info_label.setText(f"Total pages: {self.total_pages}")
                
                # Update spinbox and slider maximum
                self.pages_spinbox.setMaximum(self.total_pages)
                self.pages_slider.setMaximum(self.total_pages)
                
                # Update slider labels
                self.slider_max_label.setText(str(self.total_pages))
                
                # Enable options and actions
                self.options_section.setEnabled(True)
                self.actions_section.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read PDF:\n{str(e)}")

    def clear_file(self):
        """Clear selected file."""
        self.input_file = None
        self.total_pages = 0
        self.file_label.setText("No file selected")
        self.page_info_label.setText("")
        self.pages_spinbox.setMaximum(1)
        self.pages_spinbox.setValue(1)
        self.pages_slider.setMaximum(1)
        self.pages_slider.setValue(1)
        self.slider_max_label.setText("1")
        self.options_section.setEnabled(False)
        self.actions_section.setEnabled(False)

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
            
            QLabel#pageInfoLabel {
                font-size: 13px;
                color: #6c757d;
                font-weight: 500;
            }
            
            QLabel#sliderLabel {
                font-size: 12px;
                color: #6c757d;
                min-width: 30px;
            }
        """)
