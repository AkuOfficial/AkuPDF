import os
from pypdf import PdfWriter


class Merger:
    def __init__(self):
        self.engine = PdfWriter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.engine.close()

    def process(self, input_files: list[str], output_file: str = "merged.pdf"):
        if not input_files:
            raise ValueError("No input files provided for merging")

        if os.path.exists(output_file):
            raise FileExistsError(f"Output file already exists: {output_file}")

        for pdf in input_files:
            self.engine.append(pdf)

        self.engine.write(output_file)
