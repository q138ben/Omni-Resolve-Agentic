from src.tools.mcp_server import get_billing_details, check_network_outage

def test_get_billing_details_known_customer():
    response = get_billing_details("CUST-001")
    assert "$75.50" in response
    assert "Paid" in response

def test_get_billing_details_unknown_customer():
    response = get_billing_details("UNKNOWN")
    assert "Not Found" in response

def test_check_network_outage_exists():
    response = check_network_outage("90210")
    assert "service disruption" in response

def test_check_network_outage_normal():
    response = check_network_outage("55555")
    assert "operating normally" in response
