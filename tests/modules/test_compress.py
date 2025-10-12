import pytest
import os
from pathlib import Path
from pypdf import PdfReader
from src.modules.compress import Compressor


@pytest.fixture
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent.parent / "data"


def test_compress_basic(tmp_path, test_data_dir):
    """Test basic PDF compression."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "sample.pdf")) as compressor:
        stats = compressor.compress(str(output_path))
    
    assert os.path.exists(output_path)
    assert stats["original_size"] > 0
    assert stats["compressed_size"] > 0


def test_compress_returns_stats(tmp_path, test_data_dir):
    """Test that compression returns statistics."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "big_text.pdf")) as compressor:
        stats = compressor.compress(str(output_path))
    
    assert "original_size" in stats
    assert "compressed_size" in stats
    assert "reduction_percent" in stats


def test_compress_with_level_low(tmp_path, test_data_dir):
    """Test compression with low level."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "unoptimized.pdf")) as compressor:
        stats = compressor.compress(str(output_path), level="low")
    
    assert os.path.exists(output_path)
    assert stats["reduction_percent"] > 20


def test_compress_with_level_high(tmp_path, test_data_dir):
    """Test compression with high level."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "unoptimized.pdf")) as compressor:
        stats = compressor.compress(str(output_path), level="high")
    
    assert os.path.exists(output_path)
    assert stats["reduction_percent"] > 70


def test_compress_preserves_pages(tmp_path, test_data_dir):
    """Test that compression preserves page count."""
    input_file = str(test_data_dir / "sample.pdf")
    output_path = tmp_path / "compressed.pdf"
    
    original_pages = len(PdfReader(input_file).pages)
    
    with Compressor(input_file) as compressor:
        compressor.compress(str(output_path))
    
    compressed_pages = len(PdfReader(str(output_path)).pages)
    assert compressed_pages == original_pages


def test_compress_mixed_content(tmp_path, test_data_dir):
    """Test compressing mixed content PDF."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "mixed_content.pdf")) as compressor:
        stats = compressor.compress(str(output_path))
    
    assert os.path.exists(output_path)
    assert len(PdfReader(str(output_path)).pages) == 4


def test_compress_with_images(tmp_path, test_data_dir):
    """Test compressing PDF with images."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "images.pdf")) as compressor:
        stats = compressor.compress(str(output_path))
    
    assert os.path.exists(output_path)
    assert stats["compressed_size"] > 0


def test_compress_multipage_text(tmp_path, test_data_dir):
    """Test compressing multipage text PDF."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "multipage_text.pdf")) as compressor:
        stats = compressor.compress(str(output_path))
    
    assert os.path.exists(output_path)
    assert len(PdfReader(str(output_path)).pages) == 6


def test_compress_large_file(tmp_path, test_data_dir):
    """Test compressing large PDF file."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "large_file.pdf")) as compressor:
        stats = compressor.compress(str(output_path), level="medium")
    
    assert os.path.exists(output_path)
    assert stats["original_size"] > 1024 * 1024
    assert stats["compressed_size"] > 0


def test_compress_heavy_mixed(tmp_path, test_data_dir):
    """Test compressing heavy mixed content PDF."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "heavy_mixed.pdf")) as compressor:
        stats = compressor.compress(str(output_path), level="high")
    
    assert os.path.exists(output_path)
    assert stats["original_size"] > 2 * 1024 * 1024
    assert stats["compressed_size"] < stats["original_size"]


def test_compress_unoptimized(tmp_path, test_data_dir):
    """Test compressing unoptimized PDF with images."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "unoptimized.pdf")) as compressor:
        stats = compressor.compress(str(output_path), level="medium")
    
    assert os.path.exists(output_path)
    assert stats["original_size"] > 4 * 1024 * 1024
    assert stats["compressed_size"] < stats["original_size"]
    assert stats["reduction_percent"] > 50


def test_compress_unoptimized_high(tmp_path, test_data_dir):
    """Test high compression on unoptimized PDF."""
    output_path = tmp_path / "compressed.pdf"
    with Compressor(str(test_data_dir / "unoptimized.pdf")) as compressor:
        stats = compressor.compress(str(output_path), level="high")
    
    assert os.path.exists(output_path)
    assert stats["original_size"] > 4 * 1024 * 1024
    assert stats["compressed_size"] < stats["original_size"]
    assert stats["reduction_percent"] > 70


def test_get_compression_levels():
    """Test getting available compression levels."""
    levels = Compressor.get_compression_levels()
    assert "low" in levels
    assert "medium" in levels
    assert "high" in levels
