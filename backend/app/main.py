from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from core.runtime.container import create_container
from core.system.status import build_status


app = FastAPI(
    title="SURAYA AI",
    version="0.4.0",
    description="Private Personal AI Operating System",
)

container = create_container()


class CommandRequest(BaseModel):
    command: str = Field(..., min_length=1)
    session_id: str | None = None


class MemoryRequest(BaseModel):
    value: Any


class SecretRequest(BaseModel):
    value: str = Field(..., min_length=1)


class CloudUploadRequest(BaseModel):
    local_path: str
    remote_path: str
    provider: str = "local"


class PermissionRequest(BaseModel):
    name: str


class ApprovalRequestBody(BaseModel):
    approval_id: str


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "name": "SURAYA AI",
        "version": "0.4.0",
        "status": "online",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    status = build_status(container)

    return {
        "status": "healthy",
        "runtime_running": status.runtime_running,
        "emergency_stop": status.emergency_stop,
        "tools": status.tool_count,
        "cloud_providers": status.cloud_provider_count,
        "pending_approvals": status.pending_approvals,
    }


@app.get("/status")
def system_status() -> dict[str, Any]:
    status = build_status(container)

    return {
        "name": status.name,
        "version": status.version,
        "runtime_running": status.runtime_running,
        "emergency_stop": status.emergency_stop,
        "tool_count": status.tool_count,
        "cloud_provider_count": status.cloud_provider_count,
        "pending_approvals": status.pending_approvals,
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


@app.post("/command")
def command(request: CommandRequest) -> dict[str, Any]:
    if not container.runtime.running:
        raise HTTPException(
            status_code=503,
            detail="SURAYA runtime is stopped.",
        )

    return container.runtime.handle_command(
        request.command,
        session_id=request.session_id,
    )


@app.post("/runtime/start")
def start_runtime() -> dict[str, Any]:
    container.runtime.start()

    return {
        "status": "started",
        "running": container.runtime.running,
    }


@app.post("/runtime/stop")
def stop_runtime() -> dict[str, Any]:
    container.runtime.stop()

    return {
        "status": "stopped",
        "running": container.runtime.running,
    }


@app.post("/runtime/emergency-stop")
def emergency_stop() -> dict[str, Any]:
    container.runtime.emergency_stop()

    return {
        "status": "emergency_stopped",
        "running": container.runtime.running,
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
    container.memory.put(
        key,
        request.value,
    )

    return {
        "status": "stored",
        "key": key,
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


@app.get("/approvals")
def approvals() -> list[dict[str, Any]]:
    return [
        {
            "id": item.id,
            "status": item.status.value,
            "reason": item.reason,
            "tool": item.action.tool,
            "action": item.action.action,
            "parameters": item.action.parameters,
        }
        for item in container.guardian.approvals.all()
    ]


@app.post("/approvals/approve")
def approve(request: ApprovalRequestBody) -> dict[str, Any]:
    try:
        item = container.guardian.approvals.approve(
            request.approval_id
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Approval request not found.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return {
        "id": item.id,
        "status": item.status.value,
    }


@app.post("/approvals/deny")
def deny(request: ApprovalRequestBody) -> dict[str, Any]:
    try:
        item = container.guardian.approvals.deny(
            request.approval_id
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Approval request not found.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return {
        "id": item.id,
        "status": item.status.value,
    }


@app.get("/permissions")
def permissions() -> list[dict[str, Any]]:
    return [
        {
            "name": item.name,
            "description": item.description,
            "granted": item.granted,
            "metadata": item.metadata,
        }
        for item in container.permissions.list()
    ]


@app.post("/permissions/{name}/grant")
def grant_permission(name: str) -> dict[str, Any]:
    permission = container.permissions.grant(name)

    return {
        "name": permission.name,
        "granted": permission.granted,
    }


@app.post("/permissions/{name}/revoke")
def revoke_permission(name: str) -> dict[str, Any]:
    permission = container.permissions.revoke(name)

    return {
        "name": permission.name,
        "granted": permission.granted,
    }


@app.put("/secrets/{key}")
def set_secret(
    key: str,
    request: SecretRequest,
) -> dict[str, Any]:
    container.secrets.set(
        key,
        request.value,
    )

    return {
        "status": "stored",
        "key": key,
    }


@app.delete("/secrets/{key}")
def delete_secret(key: str) -> dict[str, Any]:
    deleted = container.secrets.delete(key)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Secret not found.",
        )

    return {
        "status": "deleted",
        "key": key,
    }


@app.get("/cloud/providers")
def cloud_providers() -> list[str]:
    return container.cloud.list_providers()


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
