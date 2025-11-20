from typing import Dict


def build_extraction_prompt(claim_text: str) -> Dict:
    return {
        "role": "user",
        "content": [{
            "text": (
                "Extract the following structured fields as JSON keys with concise values:\n"
                "- claimant_name\n- incident_date\n- claim_type\n- policy_number\n- amount_requested\n"
                "If unavailable, use null. Do not include extra keys.\n\n"
                f"Claim text:\n{claim_text}"
            )
        }]
    }


def build_summary_prompt(claim_text: str, policy_context: str) -> Dict:
    return {
        "role": "user",
        "content": [{
            "text": (
                "Summarize this insurance claim in 5-7 sentences for a claims examiner. "
                "Include key facts, estimated severity, and any policy constraints from the provided context."
                "\n\nPolicy context:\n"
                f"{policy_context}\n\n"
                "Claim text:\n"
                f"{claim_text}"
            )
        }]
    }


