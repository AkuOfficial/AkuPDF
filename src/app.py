import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QFont

from src.ui.main_window import MainWindow


def apply_modern_theme(app):
    """Apply a modern light theme to the application."""
    # Set application style to Fusion for better cross-platform appearance
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Set a modern font
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)
    
    # Apply global styles
    app.setStyleSheet("""
        QApplication {
            background-color: #f8f9fa;
            color: #212529;
        }
        
        QScrollBar:vertical {
            background: #f1f3f4;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #dadce0;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #bdc1c6;
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)


def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Apply the modern theme
    apply_modern_theme(app)
    
    # Set application name and organization
    app.setApplicationName("AkuPDF")
    app.setOrganizationName("AkuPDF")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()