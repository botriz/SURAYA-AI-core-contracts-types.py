from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock

from cryptography.fernet import Fernet, InvalidToken


class SecretStore:
    """Encrypted local secret store. Requires a Fernet key from the secret manager."""

    def __init__(self, path: str = "data/secrets.enc", key: str | bytes | None = None) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        configured_key = key if key is not None else os.environ.get("SURAYA_SECRET_KEY")
        if isinstance(configured_key, str):
            configured_key = configured_key.encode("ascii", errors="strict")
        try:
            self._fernet = Fernet(configured_key) if configured_key else None
        except (ValueError, TypeError) as exc:
            raise ValueError("SURAYA_SECRET_KEY must be a valid Fernet key.") from exc
        self._lock = Lock()

    def _require_cipher(self) -> Fernet:
        if self._fernet is None:
            raise RuntimeError("Encrypted secret storage is not configured.")
        return self._fernet

    def _read(self) -> dict[str, str]:
        cipher = self._require_cipher()
        if not self.path.exists():
            return {}
        try:
            plaintext = cipher.decrypt(self.path.read_bytes())
            value = json.loads(plaintext.decode("utf-8"))
        except (InvalidToken, UnicodeDecodeError, json.JSONDecodeError, OSError) as exc:
            raise RuntimeError("Encrypted secret store cannot be authenticated or read.") from exc
        if not isinstance(value, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in value.items()
        ):
            raise RuntimeError("Encrypted secret store has an invalid format.")
        return value

    def _write(self, data: dict[str, str]) -> None:
        cipher = self._require_cipher()
        encrypted = cipher.encrypt(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(encrypted)
                stream.flush()
                os.fsync(stream.fileno())
        finally:
            if temporary.exists():
                os.chmod(temporary, 0o600)
        os.replace(temporary, self.path)
        os.chmod(self.path, 0o600)

    def set(self, key: str, value: str) -> None:
        normalized = key.strip()
        if not normalized:
            raise ValueError("Secret key cannot be empty.")
        if not isinstance(value, str) or not value:
            raise ValueError("Secret value cannot be empty.")
        with self._lock:
            data = self._read()
            data[normalized] = value
            self._write(data)

    def get(self, key: str) -> str | None:
        with self._lock:
            return self._read().get(key)

    def delete(self, key: str) -> bool:
        with self._lock:
            data = self._read()
            if key not in data:
                return False
            del data[key]
            self._write(data)
            return True

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def list_keys(self) -> list[str]:
        with self._lock:
            return sorted(self._read().keys())
