from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Opportunity:
    problem: str
    proposed_solution: str
    target_market: str
    revenue_model: str
    risks: list[str] = field(default_factory=list)
    validation_steps: list[str] = field(default_factory=list)


class WealthEngine:
    """
    Business opportunity analysis layer.

    It generates and evaluates opportunities; it does not guarantee
    financial outcomes or autonomously commit capital.
    """

    def evaluate(
        self,
        problem: str,
        solution: str,
        market: str,
        revenue_model: str,
    ) -> Opportunity:
        return Opportunity(
            problem=problem,
            proposed_solution=solution,
            target_market=market,
            revenue_model=revenue_model,
            risks=[
                "Market demand may be lower than expected.",
                "Competition may reduce margins.",
                "Execution costs may exceed assumptions.",
            ],
            validation_steps=[
                "Define the target customer.",
                "Validate the problem with real users.",
                "Build the smallest useful prototype.",
                "Measure willingness to pay.",
                "Track acquisition cost and retention.",
                "Only scale after evidence supports the model.",
            ],
        )
