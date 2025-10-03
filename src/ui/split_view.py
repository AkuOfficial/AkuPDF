from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QFrame, QSpinBox, QSlider, QLineEdit
)
from PySide6.QtCore import Qt, QTimer
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

        # Status message
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        layout.addWidget(self.status_label)

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
        self.file_label.setWordWrap(True)
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

        options_header = QLabel("Options")
        options_header.setProperty("class", "list-header")
        layout.addWidget(options_header)

        # Split: Pages per file option with slider
        split_label = QLabel("Split - Pages per file:")
        split_label.setObjectName("optionLabel")
        layout.addWidget(split_label)
        
        pages_layout = QHBoxLayout()
        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setMinimum(1)
        self.pages_spinbox.setMaximum(1)
        self.pages_spinbox.setValue(1)
        self.pages_spinbox.valueChanged.connect(self._sync_slider_from_spinbox)
        pages_layout.addWidget(self.pages_spinbox)
        pages_layout.addStretch()
        layout.addLayout(pages_layout)
        
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
        
        layout.addLayout(slider_container)

        # Extract: Page numbers input
        extract_label = QLabel("Extract - Page numbers (e.g., 1,3,5-7):")
        extract_label.setObjectName("optionLabel")
        layout.addWidget(extract_label)
        
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Enter page numbers...")
        layout.addWidget(self.pages_input)

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

        extract_btn = QPushButton("📄  Extract Pages")
        extract_btn.setProperty("class", "secondary-button")
        extract_btn.clicked.connect(self.extract_pages)
        layout.addWidget(extract_btn)

        split_btn = QPushButton("✂️  Split PDF")
        split_btn.setProperty("class", "primary-button")
        split_btn.clicked.connect(self.split_file)
        layout.addWidget(split_btn)

        return container

    def _show_status(self, message, is_error=False):
        """Show status message inline."""
        self.status_label.setText(message)
        self.status_label.setProperty("error", is_error)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.show()
        
        # Auto-hide after 5 seconds
        QTimer.singleShot(5000, self.status_label.hide)

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

    def _parse_page_numbers(self, text):
        """Parse page numbers from text input (e.g., '1,3,5-7' -> [0,2,4,5,6])."""
        pages = set()
        try:
            for part in text.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    start, end = int(start.strip()), int(end.strip())
                    pages.update(range(start - 1, end))
                else:
                    pages.add(int(part) - 1)
            return sorted(pages)
        except:
            return None

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
                    self._show_status("⚠️ The selected PDF has no pages and cannot be split.", True)
                    return
                
                self.input_file = file
                self.file_label.setText(file)
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
                self._show_status(f"❌ Failed to read PDF: {str(e)}", True)

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
        self.pages_input.clear()
        self.options_section.setEnabled(False)
        self.actions_section.setEnabled(False)

    def split_file(self):
        """Split the PDF file."""
        if not self.input_file:
            self._show_status("⚠️ Please select a PDF file to split.", True)
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            try:
                with Splitter(self.input_file) as splitter:
                    pages_per_file = self.pages_spinbox.value()
                    file_count = splitter.split_by_pages(output_dir, pages_per_file)
                self._show_status(f"✅ PDF split successfully! Created {file_count} files in: {output_dir}")
                self.clear_file()
            except Exception as e:
                self._show_status(f"❌ Failed to split PDF: {str(e)}", True)

    def extract_pages(self):
        """Extract specific pages from PDF."""
        if not self.input_file:
            self._show_status("⚠️ Please select a PDF file to extract pages from.", True)
            return

        page_text = self.pages_input.text().strip()
        if not page_text:
            self._show_status("⚠️ Please enter page numbers to extract.", True)
            return

        page_numbers = self._parse_page_numbers(page_text)
        if page_numbers is None:
            self._show_status("❌ Invalid page numbers format. Use format like: 1,3,5-7", True)
            return

        if not page_numbers:
            self._show_status("⚠️ No valid page numbers specified.", True)
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Extracted Pages", "extracted.pdf", "PDF Files (*.pdf)"
        )
        if output_file:
            try:
                with Splitter(self.input_file) as splitter:
                    splitter.extract_pages(output_file, page_numbers)
                self._show_status(f"✅ Pages extracted successfully! Saved to: {output_file}")
                self.clear_file()
            except Exception as e:
                self._show_status(f"❌ Failed to extract pages: {str(e)}", True)

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
            
            QLabel#optionLabel {
                font-size: 13px;
                font-weight: 600;
                color: #495057;
                margin-top: 8px;
            }
            
            QLabel#sliderLabel {
                font-size: 12px;
                color: #6c757d;
                min-width: 30px;
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
