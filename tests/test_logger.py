from utils.logger import _redact

def test_redact():
    text = """
    Email: user@domain.com
    Phone: +1-555-123-4567
    """
    redacted = _redact(text)
    assert "[redacted-email]" in redacted
    assert "[redacted-phone]" in redacted