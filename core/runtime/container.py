from __future__ import annotations

from dataclasses import dataclass

from core.audit.log import AuditLog
from core.brain.brain import Brain
from core.cloud.local_provider import LocalStorageProvider
from core.cloud.manager import CloudStorageManager
from core.executor.runtime import Executor
from core.guardian.guardian import Guardian
from core.memory.store import MemoryStore
from core.models.providers import create_default_model_router
from core.runtime.system import SurayaRuntime
from core.security.permissions import PermissionManager
from core.security.secrets import SecretStore
from core.tools.builtin import register_builtin_tools
from core.tools.registry import ToolRegistry


@dataclass
class SurayaContainer:
    memory: MemoryStore
    audit: AuditLog
    tools: ToolRegistry
    executor: Executor
    brain: Brain
    guardian: Guardian
    cloud: CloudStorageManager
    permissions: PermissionManager
    secrets: SecretStore
    runtime: SurayaRuntime


def create_container(
    *,
    data_dir: str = "data",
    audit_path: str = "data/audit.jsonl",
) -> SurayaContainer:
    memory = MemoryStore(
        f"{data_dir}/memory.db"
    )

    audit = AuditLog(
        audit_path
    )

    tools = ToolRegistry()
    executor = Executor()

    model_router = create_default_model_router()

    brain = Brain(
        memory=memory,
        model_router=model_router,
    )

    guardian = Guardian()

    cloud = CloudStorageManager(
        default_provider="local",
    )

    cloud.register(
        LocalStorageProvider(
            root=f"{data_dir}/cloud",
        )
    )

    permissions = PermissionManager()

    secrets = SecretStore(
        f"{data_dir}/secrets.json",
    )

    runtime = SurayaRuntime(
        brain=brain,
        guardian=guardian,
        executor=executor,
        tools=tools,
        audit=audit,
    )

    register_builtin_tools(
        tools,
        executor,
    )

    return SurayaContainer(
        memory=memory,
        audit=audit,
        tools=tools,
        executor=executor,
        brain=brain,
        guardian=guardian,
        cloud=cloud,
        permissions=permissions,
        secrets=secrets,
        runtime=runtime,
    )
