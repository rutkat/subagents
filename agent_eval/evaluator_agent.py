import json

from llm_client import call_llm


class EvaluatorAgent:

    def __init__(
        self,
        base_url: str,
        model: str,
    ):
        self.base_url = base_url
        self.model = model

    def evaluate(
        self,
        task: str,
        candidate: str,
    ) -> dict:

        prompt = f"""
Evaluate the candidate response.

TASK:
{task}

CANDIDATE:
{candidate}

Return ONLY valid JSON.

Rules:
- score must be an integer from 0 to 10
- approved must be false when score < 6
- approved must be true when score >= 6
- feedback must explain deficiencies

Schema:

{{
  "approved": boolean,
  "score": integer,
  "feedback": string
}}
"""

        result = call_llm(
            base_url=self.base_url,
            model=self.model,
            system_prompt=(
                "You are a strict reviewer. "
                "Return only JSON."
            ),
            user_prompt=prompt,
            temperature=0.5,
        )

        try:
            review = json.loads(result)

            required_fields = [
                "approved",
                "score",
                "feedback"
            ]

            for field in required_fields:
                if field not in review:
                    raise ValueError(
                        f"Missing field: {field}"
                    )
            return review

        except Exception:
            return {
                "approved": False,
                "score": 0,
                "feedback": (
                    "Reviewer returned invalid JSON."
                ),
            }



