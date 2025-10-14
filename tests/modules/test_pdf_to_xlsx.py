import pytest
import os
from src.modules.pdf_to_xlsx import PdfToXlsxConverter


@pytest.fixture
def sample_pdf():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests", "data", "sample.pdf")


@pytest.fixture
def output_xlsx(tmp_path):
    return str(tmp_path / "output.xlsx")


def test_basic_conversion(sample_pdf, output_xlsx):
    """Test basic PDF to XLSX conversion."""
    with PdfToXlsxConverter(sample_pdf) as converter:
        result = converter.convert(output_xlsx)
    
    assert os.path.exists(output_xlsx)
    assert result["output_size"] > 0
    assert "table_count" in result


def test_extract_all_pages(sample_pdf, output_xlsx):
    """Test extracting tables from all pages."""
    with PdfToXlsxConverter(sample_pdf) as converter:
        result = converter.convert(output_xlsx, extract_all_pages=True)
    
    assert os.path.exists(output_xlsx)
    assert result["table_count"] >= 0


def test_extract_first_page_only(sample_pdf, output_xlsx):
    """Test extracting tables from first page only."""
    with PdfToXlsxConverter(sample_pdf) as converter:
        result = converter.convert(output_xlsx, extract_all_pages=False)
    
    assert os.path.exists(output_xlsx)
