from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import Lock
from uuid import uuid4

from core.contracts.types import ActionRequest


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


@dataclass
class ApprovalRequest:
    id: str
    action: ActionRequest
    status: ApprovalStatus = ApprovalStatus.PENDING
    reason: str = ""


class ApprovalManager:
    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._lock = Lock()

    def create(
        self,
        action: ActionRequest,
        reason: str = "",
    ) -> ApprovalRequest:
        request = ApprovalRequest(
            id=str(uuid4()),
            action=action,
            reason=reason,
        )

        with self._lock:
            self._requests[request.id] = request

        return request

    def get(self, request_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._requests.get(request_id)

    def approve(self, request_id: str) -> ApprovalRequest:
        with self._lock:
            request = self._requests[request_id]
            request.status = ApprovalStatus.APPROVED
            return request

    def deny(self, request_id: str) -> ApprovalRequest:
        with self._lock:
            request = self._requests[request_id]
            request.status = ApprovalStatus.DENIED
            return request

    def pending(self) -> list[ApprovalRequest]:
        with self._lock:
            return [
                request
                for request in self._requests.values()
                if request.status == ApprovalStatus.PENDING
            ]
