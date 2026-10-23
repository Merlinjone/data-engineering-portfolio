# Local unit tests for reusable quality-rule logic; run with: pytest -q
def is_valid_order(order_id, customer_id):
    return (
        order_id is not None and str(order_id).strip() != ""
        and customer_id is not None and str(customer_id).strip() != ""
    )

def test_valid_order():
    assert is_valid_order("order-1", "customer-1")

def test_missing_order_id_is_invalid():
    assert not is_valid_order(None, "customer-1")

def test_blank_order_id_is_invalid():
    assert not is_valid_order("  ", "customer-1")

def test_missing_customer_is_invalid():
    assert not is_valid_order("order-1", None)
