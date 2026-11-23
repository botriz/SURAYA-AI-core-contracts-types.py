from pathlib import Path

import pytest
from cryptography.fernet import Fernet

from core.audit.log import AuditLog
from core.cloud.local_provider import LocalStorageProvider
from core.memory.store import MemoryStore
from core.security.secrets import SecretStore


def test_memory_store_round_trip_and_delete(tmp_path: Path):
    store = MemoryStore(str(tmp_path / "memory.db"))
    store.put("profile", {"language": "fa", "count": 2})
    assert store.get("profile") == {"language": "fa", "count": 2}
    assert store.delete("profile") is True
    assert store.get("profile") is None
    store.close()


def test_audit_log_appends_structured_events(tmp_path: Path):
    log = AuditLog(str(tmp_path / "audit.jsonl"))
    log.append("test.event", {"ok": True})
    assert log.read_all()[0]["event_type"] == "test.event"
    assert log.read_all()[0]["payload"]["ok"] is True


def test_secret_store_encrypts_values_at_rest(tmp_path: Path):
    path = tmp_path / "secrets.enc"
    store = SecretStore(str(path), key=Fernet.generate_key())
    store.set("provider", "sensitive-value")
    assert b"sensitive-value" not in path.read_bytes()
    assert store.get("provider") == "sensitive-value"
    assert store.list_keys() == ["provider"]
    assert store.delete("provider") is True
    assert store.get("provider") is None


def test_secret_store_fails_closed_without_key(tmp_path: Path):
    store = SecretStore(str(tmp_path / "secrets.enc"), key=None)
    with pytest.raises(RuntimeError):
        store.set("provider", "secret")


def test_local_storage_rejects_path_traversal(tmp_path: Path):
    root = tmp_path / "cloud"
    provider = LocalStorageProvider(str(root))
    source = root / "source.txt"
    source.write_text("safe", encoding="utf-8")
    assert provider.upload(str(source), "backups/source.txt") == "backups/source.txt"
    assert (root / "backups" / "source.txt").read_text(encoding="utf-8") == "safe"
    with pytest.raises(ValueError):
        provider.upload(str(source), "../outside.txt")
    with pytest.raises(ValueError):
        provider.upload(str(tmp_path / "outside.txt"), "outside.txt")
