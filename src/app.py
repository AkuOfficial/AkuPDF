import sys
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from src.ui.main_window import MainWindow


def apply_custom_theme(app):
    """Apply custom modern theme with qt-material enhancements."""
    # Use qt-material for base components but override with custom styles
    apply_stylesheet(
        app,
        theme="light_blue.xml",
        extra={
            "density_scale": "0",
            "font_family": "Segoe UI",
            "font_size": "10px",
        },
    )

    # Override with our custom modern styles
    app.setStyleSheet(
        app.styleSheet()
        + """
        QMainWindow {
            background: #f8f9fa;
        }
        
        QFrame[class="sidebar"] {
            background: #ffffff;
            border-right: 1px solid #e9ecef;
        }
        
        QWidget[class="title-container"] {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #667eea, stop:1 #764ba2);
            border: none;
        }
        
        QLabel[class="app-title"] {
            font-size: 24px;
            font-weight: 700;
            color: white;
        }
        
        QLabel[class="app-subtitle"] {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        QPushButton[class="nav-button"] {
            text-align: left;
            padding: 16px 20px;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 500;
            color: #495057;
            background: transparent;
            margin: 2px 0;
        }
        
        QPushButton[class="nav-button"]:hover {
            background: #f8f9fa;
            color: #212529;
        }
        
        QPushButton[class="nav-button"][active="true"] {
            background: #e3f2fd;
            color: #1976d2;
            font-weight: 600;
        }
    """
    )


def main():
    app = QApplication(sys.argv)

    apply_custom_theme(app)

    app.setApplicationName("AkuPDF")
    app.setOrganizationName("AkuPDF")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
