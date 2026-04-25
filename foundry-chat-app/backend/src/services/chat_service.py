"""Chat service that delegates to a Foundry agent thread."""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import List

from services.agent_service import AgentService
from services.foundry_client import FoundryClient


class ChatService:
    def __init__(
        self,
        foundry_client: FoundryClient | None = None,
        agent_service: AgentService | None = None,
    ) -> None:
        self.foundry_client = foundry_client or FoundryClient()
        self.agent_service = agent_service or AgentService(self.foundry_client)
        self._local_history: List[dict] = []
        self._lock = threading.Lock()

    def _build_local_message(self, sender: str, text: str) -> dict:
        return {
            "id": len(self._local_history) + 1,
            "sender": sender,
            "text": text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def send_message(self, message: str) -> List[dict]:
        if self.foundry_client.is_configured:
            self.agent_service.get_or_create_agent()
            return self.foundry_client.send_message(message)

        with self._lock:
            self._local_history.append(self._build_local_message("user", message))
            self._local_history.append(
                self._build_local_message("assistant", f"Local echo: {message}")
            )
            return list(self._local_history)

    def receive_messages(self) -> List[dict]:
        if self.foundry_client.is_configured:
            return self.foundry_client.list_messages()
        with self._lock:
            return list(self._local_history)

    def reset(self) -> None:
        if self.foundry_client.is_configured:
            self.foundry_client.reset_thread()
        with self._lock:
            self._local_history.clear()
