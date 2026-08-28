import re
from pydantic import ValidationError
from schema import BookRecord


def normalize(raw: dict):
    """Returns (validated_dict, None) on success, or (None, error_dict) on failure."""
    try:
        price_match = re.search(r"[\d.]+", raw["price_text"])
        if not price_match:
            raise ValueError(f"Could not parse price from '{raw['price_text']}'")
        price_gbp = float(price_match.group())

        candidate = {**raw, "price_gbp": price_gbp}
        record = BookRecord(**candidate)
        return record.model_dump(mode="json"), None

    except (ValidationError, ValueError, KeyError) as e:
        return None, {"record": raw, "reason": str(e)}