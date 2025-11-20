from typing import Dict, Any


REQUIRED_KEYS = ["claimant_name", "incident_date", "claim_type", "policy_number", "amount_requested"]


def validate_extraction(extracted: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure required keys exist; if missing, set to None.
    Trim obviously overlong fields.
    """
    result = dict(extracted or {})
    for k in REQUIRED_KEYS:
        if k not in result:
            result[k] = None
        # cap long fields
        if isinstance(result[k], str) and len(result[k]) > 500:
            result[k] = result[k][:500]
    return result


