import sys
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from src.ui.main_window import MainWindow


def apply_custom_theme(app):
    """Apply futuristic modern theme."""
    # Use dark theme as base
    apply_stylesheet(
        app,
        theme="dark_cyan.xml",
        extra={
            "density_scale": "0",
            "font_family": "Segoe UI",
            "font_size": "10px",
        },
    )

    # Override with futuristic styles
    app.setStyleSheet(
        app.styleSheet()
        + """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #0a0e27, stop:1 #16213e);
        }
        
        QFrame[class="sidebar"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1a1f3a, stop:1 #0f1729);
            border-right: 2px solid #00d9ff;
        }
        
        QWidget[class="title-container"] {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #00d9ff, stop:1 #7b2cbf);
            border: none;
        }
        
        QLabel[class="app-title"] {
            font-size: 26px;
            font-weight: 700;
            color: white;
            letter-spacing: 2px;
        }
        
        QLabel[class="app-subtitle"] {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.7);
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        
        QPushButton[class="nav-button"] {
            text-align: left;
            padding: 16px 20px;
            border: none;
            border-left: 3px solid transparent;
            border-radius: 0px;
            font-size: 14px;
            font-weight: 500;
            color: #8892b0;
            background: transparent;
            margin: 4px 0;
        }
        
        QPushButton[class="nav-button"]:hover {
            background: rgba(0, 217, 255, 0.1);
            color: #00d9ff;
            border-left: 3px solid #00d9ff;
        }
        
        QPushButton[class="nav-button"][active="true"] {
            background: rgba(0, 217, 255, 0.15);
            color: #00d9ff;
            border-left: 3px solid #00d9ff;
            font-weight: 600;
        }
        
        QScrollBar:vertical {
            background: #1a1f3a;
            width: 10px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background: #00d9ff;
            border-radius: 5px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #00b8d4;
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
