import os
from pathlib import Path

import pytest
from pypdf import PdfReader
from src.modules.merge import Merger

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def count_pages(pdf_path: str) -> int:
    return len(PdfReader(pdf_path).pages)


class TestMerger:
    @pytest.fixture
    def tmp_output(self, tmp_path: Path) -> Path:
        return tmp_path / "output.pdf"

    def test_basic_merge(self, tmp_output):
        with Merger() as merger:
            merger.process([path("sample.pdf"), path("blank.pdf")], str(tmp_output))
        assert count_pages(str(tmp_output)) == count_pages(
            path("sample.pdf")
        ) + count_pages(path("blank.pdf"))

    def test_multiple_files(self, tmp_output):
        files = [path(f"multi_small_{i}.pdf") for i in range(3)]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        expected_pages = sum(count_pages(f) for f in files)
        assert count_pages(str(tmp_output)) == expected_pages

    def test_large_file(self, tmp_output):
        files = [path("big_text.pdf"), path("big_text.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) > 100

    def test_annotations_preserved(self, tmp_output):
        files = [path("with_notes.pdf"), path("with_notes.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_acroforms_merge(self, tmp_output):
        files = [path("with_forms.pdf"), path("sample.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_scanned_pdf_merge(self, tmp_output):
        files = [path("scan_like.pdf"), path("multi_small_0.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_empty_input(self, tmp_output):
        with Merger() as merger:
            with pytest.raises(ValueError):
                merger.process([], str(tmp_output))

    def test_missing_file(self, tmp_output):
        with Merger() as merger:
            with pytest.raises(FileNotFoundError):
                merger.process(
                    [path("does_not_exist.pdf"), path("sample.pdf")], str(tmp_output)
                )

    def test_duplicate_files(self, tmp_output):
        with Merger() as merger:
            merger.process([path("sample.pdf"), path("sample.pdf")], str(tmp_output))
        assert count_pages(str(tmp_output)) == 2 * count_pages(path("sample.pdf"))

    def test_mixed_page_sizes(self, tmp_output):
        files = [path("sample.pdf"), path("landscape.pdf"), path("a6size.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_utf8_pdfs(self, tmp_output):
        files = [path("utf8_text.pdf"), path("with_notes.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_many_small_files(self, tmp_output):
        files = [path("sample.pdf")] * 10
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == 10 * count_pages(path("sample.pdf"))

    def test_output_overwrite(self, tmp_path):
        orig = tmp_path / "orig.pdf"
        with open(path("sample.pdf"), "rb") as f_in, open(orig, "wb") as f_out:
            f_out.write(f_in.read())

        with Merger() as merger:
            with pytest.raises(FileExistsError):
                merger.process([str(orig)], str(orig))

    def test_mixed_content(self, tmp_output):
        files = [
            path("with_notes.pdf"),
            path("scan_like.pdf"),
            path("big_text.pdf"),
            path("utf8_text.pdf"),
            path("with_forms.pdf"),
        ]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)
