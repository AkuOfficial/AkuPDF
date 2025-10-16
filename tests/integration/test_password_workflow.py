import pytest
import os
from pypdf import PdfReader
from src.modules.encrypt import PDFEncryptor


@pytest.fixture
def sample_pdf():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample.pdf")


def test_full_encryption_decryption_workflow(sample_pdf, tmp_path):
    """Test complete workflow: encrypt then decrypt."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_pdf = str(tmp_path / "decrypted.pdf")
    password = "workflow123"
    
    # Step 1: Encrypt
    with PDFEncryptor(sample_pdf) as encryptor:
        encrypt_result = encryptor.add_password(encrypted_pdf, password)
    
    assert os.path.exists(encrypted_pdf)
    assert encrypt_result["page_count"] > 0
    
    # Verify encrypted
    reader = PdfReader(encrypted_pdf)
    assert reader.is_encrypted
    
    # Step 2: Decrypt
    with PDFEncryptor(encrypted_pdf) as encryptor:
        decrypt_result = encryptor.remove_password(decrypted_pdf, password)
    
    assert os.path.exists(decrypted_pdf)
    assert decrypt_result["page_count"] == encrypt_result["page_count"]
    
    # Verify decrypted
    reader = PdfReader(decrypted_pdf)
    assert not reader.is_encrypted


def test_user_and_owner_password_workflow(sample_pdf, tmp_path):
    """Test workflow with separate user and owner passwords."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_with_user = str(tmp_path / "decrypted_user.pdf")
    decrypted_with_owner = str(tmp_path / "decrypted_owner.pdf")
    
    user_pwd = "user123"
    owner_pwd = "owner456"
    
    # Encrypt with both passwords
    with PDFEncryptor(sample_pdf) as encryptor:
        encryptor.add_password(encrypted_pdf, user_pwd, owner_pwd)
    
    # Decrypt with user password
    with PDFEncryptor(encrypted_pdf) as encryptor:
        result1 = encryptor.remove_password(decrypted_with_user, user_pwd)
    assert os.path.exists(decrypted_with_user)
    assert result1["page_count"] > 0
    
    # Decrypt with owner password
    with PDFEncryptor(encrypted_pdf) as encryptor:
        result2 = encryptor.remove_password(decrypted_with_owner, owner_pwd)
    assert os.path.exists(decrypted_with_owner)
    assert result2["page_count"] > 0


def test_recovery_mode_workflow(sample_pdf, tmp_path):
    """Test recovery mode workflow for weak encryption."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_pdf = str(tmp_path / "decrypted.pdf")
    
    # Encrypt with weak protection (empty user password)
    with PDFEncryptor(sample_pdf) as encryptor:
        encryptor.add_password(encrypted_pdf, "", "owner123")
    
    # Attempt recovery without password
    with PDFEncryptor(encrypted_pdf) as encryptor:
        result = encryptor.remove_password(decrypted_pdf, None)
    
    assert os.path.exists(decrypted_pdf)
    assert result["page_count"] > 0
    
    # Verify decrypted
    reader = PdfReader(decrypted_pdf)
    assert not reader.is_encrypted


def test_wrong_password_workflow(sample_pdf, tmp_path):
    """Test workflow with wrong password fails gracefully."""
    encrypted_pdf = str(tmp_path / "encrypted.pdf")
    decrypted_pdf = str(tmp_path / "decrypted.pdf")
    
    # Encrypt
    with PDFEncryptor(sample_pdf) as encryptor:
        encryptor.add_password(encrypted_pdf, "correct123")
    
    # Try to decrypt with wrong password
    with PDFEncryptor(encrypted_pdf) as encryptor:
        with pytest.raises(ValueError, match="Incorrect password"):
            encryptor.remove_password(decrypted_pdf, "wrong123")
    
    # Decrypted file should not exist
    assert not os.path.exists(decrypted_pdf)
