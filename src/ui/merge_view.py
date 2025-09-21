from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget
from src.modules.merge import Merger


class MergeView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        btn_add = QPushButton("Add PDFs")
        btn_merge = QPushButton("Merge and Save")

        btn_add.clicked.connect(self.add_files)
        btn_merge.clicked.connect(self.merge_files)

        layout.addWidget(btn_add)
        layout.addWidget(btn_merge)
        self.setLayout(layout)

        self.files = []

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", "", "PDF Files (*.pdf)")
        if files:
            self.files.extend(files)
            self.file_list.addItems(files)

    def merge_files(self):
        if not self.files:
            return
        output_file, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)")
        if output_file:
            with Merger() as merger:
                merger.process(self.files, output_file)
