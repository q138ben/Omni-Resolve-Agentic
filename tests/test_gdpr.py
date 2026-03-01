from src.utils.gdpr import mask_pii, anonymize_data

def test_mask_pii_email():
    text = "Contact me at john.doe@example.com"
    masked = mask_pii(text)
    assert "[EMAIL_MASKED]" in masked
    assert "john.doe@example.com" not in masked

def test_mask_pii_phone():
    text = "My number is +1 234 567 8900"
    masked = mask_pii(text)
    assert "[PHONE_MASKED]" in masked
    assert "234 567 8900" not in masked

def test_anonymize_data():
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "details": "Call +1234567890"
    }
    anonymized = anonymize_data(data)
    assert anonymized["email"] == "[EMAIL_MASKED]"
    assert "[PHONE_MASKED]" in anonymized["details"]
    assert anonymized["name"] == "John Doe" # No rule for names yet
