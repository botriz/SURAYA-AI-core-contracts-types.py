from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from core.audit.log import AuditLog
from core.brain.brain import Brain
from core.executor.runtime import Executor
from core.guardian.guardian import Guardian
from core.memory.store import MemoryStore
from core.runtime.system import SurayaRuntime
from core.tools.registry import ToolRegistry


APP_NAME = "SURAYA AI"
APP_VERSION = "0.2.0"


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Private Personal AI Operating System",
)


memory = MemoryStore()

audit = AuditLog()

tools = ToolRegistry()

executor = Executor()

brain = Brain(
    memory=memory,
)

guardian = Guardian()

runtime = SurayaRuntime(
    brain=brain,
    guardian=guardian,
    executor=executor,
    tools=tools,
    audit=audit,
)


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


@app.get("/")
def root() -> dict:

    return {
        "system": APP_NAME,
        "version": APP_VERSION,
        "status": "online",
    }


@app.get("/health")
def health() -> dict:

    return {
        "status": "ok",
        "system": APP_NAME,
        "version": APP_VERSION,
        "runtime": (
            "running"
            if runtime.running
            else "stopped"
        ),
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

    return runtime.handle_command(
        request.text
    )


@app.post("/runtime/stop")
def stop_runtime() -> dict:

    runtime.stop()

    return {
        "status": "stopped",
        "controller": "guardian",
    }


@app.post("/runtime/start")
def start_runtime() -> dict:

    runtime.start()

    return {
        "status": "running",
        "controller": "guardian",
    }


@app.get("/memory/{key}")
def get_memory(
    key: str,
) -> dict:

    value = memory.get(
        key,
        default=None,
    )

    return {
        "key": key,
        "value": value,
    }


@app.put("/memory/{key}")
def put_memory(
    key: str,
    value: object,
) -> dict:

    memory.put(
        key,
        value,
    )

    return {
        "status": "stored",
        "key": key,
    }


@app.get("/audit")
def get_audit() -> list[dict]:

    return audit.read_all()
