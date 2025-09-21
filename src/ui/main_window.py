from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget

from src.ui.merge_view import MergeView


class MainWindow(QMainWindow):
    APPLICATION_NAME = "AkuPDF"

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._main_container()
        self._setup_stacked_widget()

        merge_view = MergeView()
        self._add_view(merge_view)

        self._set_initial_view(merge_view)

    def _setup_window(self):
        self.setWindowTitle(self.APPLICATION_NAME)
        self.setMinimumSize(900, 600)

    def _main_container(self):
        central = QWidget()
        self.layout = QVBoxLayout()
        central.setLayout(self.layout)
        self.setCentralWidget(central)

    def _setup_stacked_widget(self):
        # stacked widget to hold multiple views (merge, split, etc.)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

    def _add_view(self, view: QWidget):
        self.stack.addWidget(view)

    def _set_initial_view(self, view: QWidget):
        self.stack.setCurrentWidget(view)
