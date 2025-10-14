import pytest
import os
from src.modules.pdf_to_docx import PdfToDocxConverter


@pytest.fixture
def sample_pdf():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests", "data", "sample.pdf")


@pytest.fixture
def output_docx(tmp_path):
    return str(tmp_path / "output.docx")


def test_page_range_conversion(sample_pdf, output_docx):
    """Test conversion with page range."""
    with PdfToDocxConverter(sample_pdf) as converter:
        result = converter.convert(output_docx, start_page=0, end_page=1)
    
    assert os.path.exists(output_docx)
    assert result["output_size"] > 0


def test_multi_page_table_option(sample_pdf, output_docx):
    """Test multi-page table parsing option."""
    with PdfToDocxConverter(sample_pdf) as converter:
        result = converter.convert(output_docx, multi_page_table=True)
    
    assert os.path.exists(output_docx)
    assert result["output_size"] > 0


def test_multi_page_table_disabled(sample_pdf, output_docx):
    """Test with multi-page table parsing disabled."""
    with PdfToDocxConverter(sample_pdf) as converter:
        result = converter.convert(output_docx, multi_page_table=False)
    
    assert os.path.exists(output_docx)
    assert result["output_size"] > 0
