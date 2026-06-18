from generator_agent import GeneratorAgent
from evaluator_agent import EvaluatorAgent


class Orchestrator:

    def __init__(
        self,
        generator: GeneratorAgent,
        evaluator: EvaluatorAgent,
    ):
        self.generator = generator
        self.evaluator = evaluator

    def run(
        self,
        task: str,
        max_rounds: int = 3,
        min_score: int = 7,
    ) -> str:

        feedback = None
        best_response = ""

        for round_num in range(1, max_rounds + 1):

            print(f"\n---------ROUND {round_num}--------------")

            candidate = self.generator.generate(
                task=task,
                feedback=feedback,
            )

            review = self.evaluator.evaluate(
                task=task,
                candidate=candidate,
            )

            print("\nCandidate Response:")
            print(candidate)
            print("\nReview:")
            print(review)

            best_response = candidate

            approved = review.get(
                "approved",
                False,
            )

            score = review.get(
                "score",
                0,
            )

            if approved or score >= min_score:
                print("\nResponse accepted.")
                return candidate

            feedback = review.get(
                "feedback",
                "",
            )

        return best_response


