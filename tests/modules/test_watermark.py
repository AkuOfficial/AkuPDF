import pytest
import os
from src.modules.watermark import Watermarker


@pytest.fixture
def sample_pdf():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests", "data", "sample.pdf")


@pytest.fixture
def output_pdf(tmp_path):
    return str(tmp_path / "watermarked.pdf")


def test_basic_watermark(sample_pdf, output_pdf):
    """Test basic watermark addition."""
    with Watermarker(sample_pdf) as watermarker:
        result = watermarker.add_watermark(output_pdf, "CONFIDENTIAL")
    
    assert os.path.exists(output_pdf)
    assert result["output_size"] > 0
    assert result["page_count"] > 0


def test_watermark_with_opacity(sample_pdf, output_pdf):
    """Test watermark with custom opacity."""
    with Watermarker(sample_pdf) as watermarker:
        result = watermarker.add_watermark(output_pdf, "DRAFT", opacity=0.5)
    
    assert os.path.exists(output_pdf)
    assert result["output_size"] > 0


def test_watermark_low_opacity(sample_pdf, output_pdf):
    """Test watermark with low opacity."""
    with Watermarker(sample_pdf) as watermarker:
        result = watermarker.add_watermark(output_pdf, "SAMPLE", opacity=0.1)
    
    assert os.path.exists(output_pdf)
    assert result["output_size"] > 0
