from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI
from pydantic import BaseModel

from core.audit.log import AuditLog

from core.contracts.types import (
    ActionRequest,
    AuditEvent,
    CreatorCommand,
    EventType,
    Plan,
    RiskLevel,
)

from core.executor.runtime import Executor
from core.guardian.policy import GuardianPolicy
from core.tools.registry import ToolRegistry


APP_NAME = "SURAYA AI"
APP_VERSION = "0.1.0"


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Private Personal AI Operating System Core."
    ),
)


guardian = GuardianPolicy()

executor = Executor()

tools = ToolRegistry()

audit = AuditLog()


class CommandRequest(BaseModel):
    text: str


def echo(
    text: str,
) -> dict[str, str]:

    return {
        "message": text,
    }


tools.register(
    name="echo",
    description="Returns the supplied text.",
    handler=echo,
)

executor.register(
    tool_name="echo",
    handler=echo,
)


@app.get("/health")
def health() -> dict:

    return {
        "status": "ok",
        "system": APP_NAME,
        "version": APP_VERSION,
    }


@app.get("/tools")
def list_tools() -> list[dict[str, str]]:

    return [
        {
            "name": tool.name,
            "description": tool.description,
        }
        for tool in tools.list()
    ]


@app.post("/command")
def command(
    request: CommandRequest,
) -> dict:

    creator_command = CreatorCommand(
        text=request.text
    )

    audit.append(
        AuditEvent(
            event_type=EventType.COMMAND,
            actor="creator",
            payload={
                "command": creator_command.text,
                "command_id": creator_command.command_id,
            },
        )
    )

    action = ActionRequest(
        name="echo_command",
        tool="echo",
        arguments={
            "text": creator_command.text,
        },
        risk=RiskLevel.LOW,
    )

    plan = Plan(
        goal=creator_command.text,
        actions=[action],
    )

    audit.append(
        AuditEvent(
            event_type=EventType.PLAN,
            actor="brain",
            payload={
                "plan_id": plan.plan_id,
                "goal": plan.goal,
            },
        )
    )

    guardian_decision = guardian.check_plan(
        plan
    )

    audit.append(
        AuditEvent(
            event_type=EventType.GUARDIAN_PRECHECK,
            actor="guardian",
            payload=asdict(
                guardian_decision
            ),
        )
    )

    if guardian_decision.decision.value != "allow":

        return {
            "status": guardian_decision.decision.value,
            "reason": guardian_decision.reason,
            "plan_id": plan.plan_id,
        }

    result = executor.execute(
        action
    )

    audit.append(
        AuditEvent(
            event_type=EventType.ACTION,
            actor="executor",
            payload={
                "action": action.name,
                "success": result.success,
                "output": result.output,
                "error": result.error,
            },
        )
    )

    if not result.success:

        return {
            "status": "failed",
            "guardian": guardian_decision.reason,
            "error": result.error,
            "plan_id": plan.plan_id,
        }

    return {
        "status": "completed",
        "guardian": guardian_decision.reason,
        "result": result.output,
        "plan_id": plan.plan_id,
    }
