from __future__ import annotations

from dataclasses import dataclass
from typing import List

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore


@dataclass
class PlanStep:
    id: int
    action: str


class TaskPlanner:
    """Break user goals into actionable steps using OpenAI with a safe fallback."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key) if (api_key and OpenAI is not None) else None

    def create_plan(self, goal: str) -> List[PlanStep]:
        if self.client:
            try:
                response = self.client.responses.create(
                    model=self.model,
                    input=(
                        "Break this goal into a short numbered task list (3-8 steps). "
                        "Return plain text, one step per line:\n"
                        f"Goal: {goal}"
                    ),
                )
                lines = [line.strip(" -") for line in response.output_text.splitlines() if line.strip()]
                steps = [PlanStep(id=i + 1, action=line) for i, line in enumerate(lines)]
                if steps:
                    return steps
            except Exception:
                pass

        fallback = [
            "Clarify objective, constraints, and success criteria.",
            "Gather required files, apps, and credentials.",
            "Execute the task in small milestones.",
            "Verify output quality and fix issues.",
            "Document results and next actions.",
        ]
        return [PlanStep(id=i + 1, action=step) for i, step in enumerate(fallback)]
