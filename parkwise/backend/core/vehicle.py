"""Vehicle-number cleaning and checking."""
import re


def clean_vehicle_number(raw):
    """'ka 01 ab 1234' -> 'KA01AB1234' (remove spaces, uppercase)."""
    return re.sub(r"\s+", "", raw).upper()


def is_valid_vehicle_number(cleaned):
    """6 to 10 letters or digits only."""
    return re.fullmatch(r"[A-Z0-9]{6,10}", cleaned) is not None
