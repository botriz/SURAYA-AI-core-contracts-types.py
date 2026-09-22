from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from core.runtime.container import create_container
from core.tools.builtin import register_builtin_tools


app = FastAPI(
    title="SURAYA AI",
    version="0.3.0",
    description="Private Personal AI Operating System",
)

container = create_container()

register_builtin_tools(
    container.tools,
    container.executor,
)


class CommandRequest(BaseModel):
    command: str = Field(..., min_length=1)
    session_id: str | None = None


class MemoryRequest(BaseModel):
    value: Any


class CloudUploadRequest(BaseModel):
    local_path: str
    remote_path: str
    provider: str = "local"


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "name": "SURAYA AI",
        "version": "0.3.0",
        "status": "online",
        "runtime_running": container.runtime.running,
    }


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "healthy",
        "runtime_running": container.runtime.running,
        "tools": len(container.tools.list()),
        "cloud_providers": container.cloud.list_providers(),
    }


@app.get("/tools")
def list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "risk": tool.risk,
            "requires_approval": tool.requires_approval,
            "metadata": tool.metadata,
        }
        for tool in container.tools.list()
    ]


@app.get("/cloud/providers")
def cloud_providers() -> list[str]:
    return container.cloud.list_providers()


@app.post("/command")
def command(request: CommandRequest) -> dict[str, Any]:
    if not container.runtime.running:
        raise HTTPException(
            status_code=503,
            detail="SURAYA runtime is stopped.",
        )

    result = container.runtime.handle_command(
        request.command,
        session_id=request.session_id,
    )

    return result


@app.post("/runtime/stop")
def stop_runtime() -> dict[str, Any]:
    container.runtime.stop()

    return {
        "status": "stopped",
        "runtime_running": container.runtime.running,
    }


@app.post("/runtime/start")
def start_runtime() -> dict[str, Any]:
    container.runtime.start()

    return {
        "status": "started",
        "runtime_running": container.runtime.running,
    }


@app.get("/memory/{key}")
def get_memory(key: str) -> dict[str, Any]:
    value = container.memory.get(key)

    if value is None:
        raise HTTPException(
            status_code=404,
            detail="Memory not found.",
        )

    return {
        "key": key,
        "value": value,
    }


@app.put("/memory/{key}")
def put_memory(
    key: str,
    request: MemoryRequest,
) -> dict[str, Any]:
    container.memory.put(key, request.value)

    return {
        "status": "stored",
        "key": key,
        "value": request.value,
    }


@app.delete("/memory/{key}")
def delete_memory(key: str) -> dict[str, Any]:
    deleted = container.memory.delete(key)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Memory not found.",
        )

    return {
        "status": "deleted",
        "key": key,
    }


@app.get("/audit")
def audit() -> list[dict[str, Any]]:
    return container.audit.read_all()


@app.post("/cloud/upload")
def cloud_upload(
    request: CloudUploadRequest,
) -> dict[str, Any]:
    try:
        result = container.cloud.upload(
            local_path=request.local_path,
            remote_path=request.remote_path,
            provider=request.provider,
        )

        return {
            "status": "uploaded",
            "provider": request.provider,
            "file": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
