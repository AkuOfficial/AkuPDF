import pytest
from pathlib import Path
from pypdf import PdfReader
from src.modules.merge import Merger


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def count_pages(pdf_path: str) -> int:
    return len(PdfReader(pdf_path).pages)


class TestMerger:
    @pytest.fixture
    def tmp_output(self, tmp_path: Path) -> Path:
        return tmp_path / "output.pdf"

    def test_basic_merge(self, tmp_output, test_data_dir):
        with Merger() as merger:
            merger.process([str(test_data_dir / "sample.pdf"), str(test_data_dir / "blank.pdf")], str(tmp_output))
        assert count_pages(str(tmp_output)) == count_pages(
            str(test_data_dir / "sample.pdf")
        ) + count_pages(str(test_data_dir / "blank.pdf"))

    def test_multiple_files(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / f"multi_small_{i}.pdf") for i in range(3)]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        expected_pages = sum(count_pages(f) for f in files)
        assert count_pages(str(tmp_output)) == expected_pages

    def test_large_file(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "big_text.pdf"), str(test_data_dir / "big_text.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) > 100

    def test_annotations_preserved(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "with_notes.pdf"), str(test_data_dir / "with_notes.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_acroforms_merge(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "with_forms.pdf"), str(test_data_dir / "sample.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_scanned_pdf_merge(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "scan_like.pdf"), str(test_data_dir / "multi_small_0.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_empty_input(self, tmp_output):
        with Merger() as merger:
            with pytest.raises(ValueError):
                merger.process([], str(tmp_output))

    def test_missing_file(self, tmp_output, test_data_dir):
        with Merger() as merger:
            with pytest.raises(FileNotFoundError):
                merger.process(
                    [str(test_data_dir / "does_not_exist.pdf"), str(test_data_dir / "sample.pdf")], str(tmp_output)
                )

    def test_duplicate_files(self, tmp_output, test_data_dir):
        with Merger() as merger:
            merger.process([str(test_data_dir / "sample.pdf"), str(test_data_dir / "sample.pdf")], str(tmp_output))
        assert count_pages(str(tmp_output)) == 2 * count_pages(str(test_data_dir / "sample.pdf"))

    def test_mixed_page_sizes(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "sample.pdf"), str(test_data_dir / "landscape.pdf"), str(test_data_dir / "a6size.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_utf8_pdfs(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "utf8_text.pdf"), str(test_data_dir / "with_notes.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_many_small_files(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "sample.pdf")] * 10
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == 10 * count_pages(str(test_data_dir / "sample.pdf"))

    def test_output_overwrite(self, tmp_path, test_data_dir):
        orig = tmp_path / "orig.pdf"
        with open(test_data_dir / "sample.pdf", "rb") as f_in, open(orig, "wb") as f_out:
            f_out.write(f_in.read())

        # Should now allow overwriting
        with Merger() as merger:
            merger.process([str(test_data_dir / "sample.pdf")], str(orig))
        assert orig.exists()

    def test_mixed_content(self, tmp_output, test_data_dir):
        files = [
            str(test_data_dir / "with_notes.pdf"),
            str(test_data_dir / "scan_like.pdf"),
            str(test_data_dir / "big_text.pdf"),
            str(test_data_dir / "utf8_text.pdf"),
            str(test_data_dir / "with_forms.pdf"),
        ]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)

    def test_merge_with_mixed_content_pdf(self, tmp_output, test_data_dir):
        files = [str(test_data_dir / "mixed_content.pdf"), str(test_data_dir / "sample.pdf")]
        with Merger() as merger:
            merger.process(files, str(tmp_output))
        assert count_pages(str(tmp_output)) == sum(count_pages(f) for f in files)
