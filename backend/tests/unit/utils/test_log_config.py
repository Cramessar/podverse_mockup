# tests/utils/test_log_config.py

from app.utils.log_config import truncate_payload

def test_truncate_payload_short_strings():
    input_data = {"key": "short text"}
    assert truncate_payload(input_data) == input_data  # No change

def test_truncate_payload_long_string():
    long_value = "a" * 1100
    result = truncate_payload({"key": long_value})
    assert result["key"].startswith("a" * 1000)
    assert result["key"].endswith("...")

def test_truncate_payload_nested_dict():
    nested = {
        "outer": {
            "inner": "x" * 1200
        }
    }
    result = truncate_payload(nested)
    assert len(result["outer"]["inner"]) == 1003  # 1000 + "..."
