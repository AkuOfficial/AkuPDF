from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget

class MainWindow(QMainWindow):
    APPLICATION_NAME = "AkuPDF"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.APPLICATION_NAME)
        self.setMinimumSize(900, 600)

        # główny layout
        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # miejsce na przyszłe widoki (QStackedWidget)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # TODO: załadować widoki (merge_view, split_view, itp.)
