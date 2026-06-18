from llm_client import call_llm


class GeneratorAgent:

    def __init__(
        self,
        base_url: str,
        model: str,
    ):
        self.base_url = base_url
        self.model = model

    def generate(
        self,
        task: str,
        feedback: str | None = None,
    ) -> str:

        prompt = f"""
TASK:
{task}
"""

        if feedback:
            prompt += f"""

REVIEW FEEDBACK:
{feedback}

Revise the response and address all concerns.
"""

        return call_llm(
            base_url=self.base_url,
            model=self.model,
            system_prompt=(
                "You are a content generation agent. "
                "Produce the highest quality response."
            ),
            user_prompt=prompt,
            temperature=0.5,
        )


