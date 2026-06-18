from generator_agent import GeneratorAgent
from evaluator_agent import EvaluatorAgent
from orchestrator import Orchestrator


LLM_URL = "http://localhost:1234/v1"

GENERATOR_MODEL = "gemma-4-12b-coder-fable5-composer2.5-v1"
#GENERATOR_MODEL = "your-llm-choice"
#EVALUATOR_MODEL = "your-evaluator-choice"
EVALUATOR_MODEL = "liquid/lfm2.5-1.2b"

def main():

    generator = GeneratorAgent(
        base_url=LLM_URL,
        model=GENERATOR_MODEL,
    )

    evaluator = EvaluatorAgent(
        base_url=LLM_URL,
        model=EVALUATOR_MODEL,
    )

    orchestrator = Orchestrator(
        generator=generator,
        evaluator=evaluator,
    )

    task = """
Write a technical explanation of Retrieval Augmented Generation (RAG)
for software engineers.

Include:
- What it is
- Why it helps
- Limitations
- A simple example
"""

    result = orchestrator.run(
        task=task,
        max_rounds=3,
        min_score=1,
    )

    print("\n=== FINAL RESULT ===\n")
    print(result)


if __name__ == "__main__":
    main()


