import re

def mask_pii(text: str) -> str:
    """
    Masks common PII (Personal Identifiable Information) in compliance with GDPR.
    """
    # Simple email masking
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL_MASKED]', text)
    # Simple phone number masking (e.g., +1 234 567 8900)
    text = re.sub(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', '[PHONE_MASKED]', text)
    return text

def anonymize_data(data: dict) -> dict:
    """
    Anonymizes data dictionaries before processing.
    """
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = mask_pii(value)
    return data
