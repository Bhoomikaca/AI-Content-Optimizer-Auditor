def verify_content(audit_and_verification_result):

    try:

        verification_result = audit_and_verification_result.get(
            "verification",
            {}
        )

        return verification_result

    except Exception as error:

        print("CONTENT VERIFIER ERROR:", error)

        return {
            "supported_claims": 0,
            "unsupported_claims": 0,
            "contradicted_claims": 0,
            "verification_details": [],
            "error": "Claim verification temporarily unavailable."
        }