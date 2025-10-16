import pytest
import os
from pypdf import PdfReader
from src.modules.encrypt import PDFEncryptor


@pytest.fixture
def sample_pdf():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests", "data", "sample.pdf")


@pytest.fixture
def output_pdf(tmp_path):
    return str(tmp_path / "output.pdf")


def test_add_password(sample_pdf, output_pdf):
    """Test adding password to PDF."""
    with PDFEncryptor(sample_pdf) as encryptor:
        result = encryptor.add_password(output_pdf, "test123")
    
    assert os.path.exists(output_pdf)
    assert result["output_size"] > 0
    assert result["page_count"] > 0
    
    # Verify PDF is encrypted
    reader = PdfReader(output_pdf)
    assert reader.is_encrypted


def test_add_password_with_owner(sample_pdf, output_pdf):
    """Test adding password with separate owner password."""
    with PDFEncryptor(sample_pdf) as encryptor:
        result = encryptor.add_password(output_pdf, "user123", "owner456")
    
    assert os.path.exists(output_pdf)
    reader = PdfReader(output_pdf)
    assert reader.is_encrypted


def test_remove_password_with_password(sample_pdf, tmp_path):
    """Test removing password from PDF with password."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_pdf = str(tmp_path / "decrypted.pdf")
    password = "test123"
    
    # First encrypt
    with PDFEncryptor(sample_pdf) as encryptor:
        encryptor.add_password(encrypted_pdf, password)
    
    # Then decrypt with password
    with PDFEncryptor(encrypted_pdf) as encryptor:
        result = encryptor.remove_password(decrypted_pdf, password)
    
    assert os.path.exists(decrypted_pdf)
    assert result["output_size"] > 0
    
    # Verify PDF is not encrypted
    reader = PdfReader(decrypted_pdf)
    assert not reader.is_encrypted


def test_remove_password_without_password(sample_pdf, tmp_path):
    """Test removing password from PDF without password (recovery)."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_pdf = str(tmp_path / "decrypted.pdf")
    
    # Encrypt with only owner password (weak protection)
    with PDFEncryptor(sample_pdf) as encryptor:
        encryptor.add_password(encrypted_pdf, "", "owner123")
    
    # Try to decrypt without password
    with PDFEncryptor(encrypted_pdf) as encryptor:
        result = encryptor.remove_password(decrypted_pdf, None)
    
    assert os.path.exists(decrypted_pdf)
    assert result["output_size"] > 0


def test_remove_password_recovery_fails_with_strong_password(sample_pdf, tmp_path):
    """Test password recovery fails with strong user password."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_pdf = str(tmp_path / "decrypted.pdf")
    
    # Encrypt with strong user password
    with PDFEncryptor(sample_pdf) as encryptor:
        encryptor.add_password(encrypted_pdf, "strong123")
    
    # Try to decrypt without password should fail
    with PDFEncryptor(encrypted_pdf) as encryptor:
        with pytest.raises(ValueError, match="Cannot decrypt|strong user password"):
            encryptor.remove_password(decrypted_pdf, None)


def test_add_password_with_empty_owner(sample_pdf, output_pdf):
    """Test adding password with empty owner password uses user password."""
    with PDFEncryptor(sample_pdf) as encryptor:
        result = encryptor.add_password(output_pdf, "user123", None)
    
    assert os.path.exists(output_pdf)
    reader = PdfReader(output_pdf)
    assert reader.is_encrypted
    assert reader.decrypt("user123") > 0


def test_remove_password_wrong_password(sample_pdf, tmp_path):
    """Test removing password with wrong password fails."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_pdf = str(tmp_path / "decrypted.pdf")
    
    # First encrypt
    with PDFEncryptor(sample_pdf) as encryptor:
        encryptor.add_password(encrypted_pdf, "correct123")
    
    # Try to decrypt with wrong password
    with PDFEncryptor(encrypted_pdf) as encryptor:
        with pytest.raises(ValueError, match="Incorrect password"):
            encryptor.remove_password(decrypted_pdf, "wrong123")
