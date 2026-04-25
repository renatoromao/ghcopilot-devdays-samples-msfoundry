"""Thin wrapper around the Microsoft Foundry (Azure AI Projects) SDK."""

from __future__ import annotations

import os
import threading
from typing import List, Optional

from azure.identity import DefaultAzureCredential


class FoundryClient:
    """Manages a single Foundry agent + chat thread for the application."""

    def __init__(self) -> None:
        self.endpoint = (
            os.getenv("AZURE_AI_PROJECT_ENDPOINT")
            or os.getenv("AZURE_AIPROJECT_ENDPOINT")
            or os.getenv("FOUNDRY_PROJECT_ENDPOINT")
            or ""
        ).strip()

        self.agent_id = (os.getenv("FOUNDRY_AGENT_ID") or os.getenv("AZURE_AI_AGENT_ID") or "").strip()
        self.model_deployment = (
            os.getenv("FOUNDRY_MODEL_DEPLOYMENT")
            or os.getenv("AZURE_AI_MODEL_DEPLOYMENT")
            or ""
        ).strip()

        self.agent_name = os.getenv("AGENT_NAME", "foundry-chat-agent")
        self.agent_description = os.getenv("AGENT_DESCRIPTION", "Foundry chat application agent")
        self.agent_instructions = os.getenv(
            "AGENT_INSTRUCTIONS",
            "You are a helpful assistant for the Foundry chat application. "
            "Answer concisely and clearly.",
        )

        self._lock = threading.Lock()
        self._client = None
        self._agent = None
        self._thread_id: Optional[str] = None

    @property
    def is_configured(self) -> bool:
        return bool(self.endpoint) and (bool(self.agent_id) or bool(self.model_deployment))

    def status(self) -> dict:
        return {
            "configured": self.is_configured,
            "endpoint": self.endpoint or None,
            "agent_id": self.agent_id or None,
            "model_deployment": self.model_deployment or None,
        }

    def _get_client(self):
        if self._client is None:
            from azure.ai.agents import AgentsClient

            if not self.endpoint:
                raise RuntimeError(
                    "AZURE_AI_PROJECT_ENDPOINT is not configured. "
                    "Set it in your environment or .env file."
                )

            self._client = AgentsClient(
                endpoint=self.endpoint,
                credential=DefaultAzureCredential(),
            )
        return self._client

    def get_or_create_agent(self) -> dict:
        with self._lock:
            if self._agent is not None:
                return self._agent_to_dict(self._agent)

            client = self._get_client()

            if self.agent_id:
                self._agent = client.get_agent(self.agent_id)
            else:
                if not self.model_deployment:
                    raise RuntimeError(
                        "Either FOUNDRY_AGENT_ID or FOUNDRY_MODEL_DEPLOYMENT must be set."
                    )
                self._agent = client.create_agent(
                    model=self.model_deployment,
                    name=self.agent_name,
                    description=self.agent_description,
                    instructions=self.agent_instructions,
                )

            return self._agent_to_dict(self._agent)

    @staticmethod
    def _agent_to_dict(agent) -> dict:
        return {
            "id": getattr(agent, "id", None),
            "name": getattr(agent, "name", None),
            "description": getattr(agent, "description", None),
            "model": getattr(agent, "model", None),
        }

    def reset_thread(self) -> None:
        with self._lock:
            self._thread_id = None

    def _ensure_thread(self) -> str:
        if self._thread_id:
            return self._thread_id

        client = self._get_client()
        thread = client.threads.create()
        self._thread_id = thread.id
        return self._thread_id

    def send_message(self, message: str) -> List[dict]:
        agent = self.get_or_create_agent()
        client = self._get_client()
        thread_id = self._ensure_thread()

        client.messages.create(thread_id=thread_id, role="user", content=message)

        run = client.runs.create_and_process(thread_id=thread_id, agent_id=agent["id"])
        if getattr(run, "status", None) == "failed":
            error = getattr(run, "last_error", None)
            raise RuntimeError(f"Foundry run failed: {error}")

        return self.list_messages()

    def list_messages(self) -> List[dict]:
        if not self._thread_id:
            return []

        client = self._get_client()
        items = client.messages.list(thread_id=self._thread_id, order="asc")

        result: List[dict] = []
        for index, item in enumerate(items, start=1):
            text = self._extract_text(item)
            if not text:
                continue
            result.append(
                {
                    "id": getattr(item, "id", None) or index,
                    "sender": getattr(item, "role", "assistant"),
                    "text": text,
                    "timestamp": self._format_timestamp(item),
                }
            )
        return result

    @staticmethod
    def _extract_text(message) -> str:
        content = getattr(message, "content", None) or []
        parts: List[str] = []
        for piece in content:
            text_obj = getattr(piece, "text", None)
            if text_obj is not None:
                value = getattr(text_obj, "value", None)
                if value:
                    parts.append(value)
                    continue
            value = getattr(piece, "value", None)
            if value:
                parts.append(str(value))
        return "\n".join(parts).strip()

    @staticmethod
    def _format_timestamp(message) -> Optional[str]:
        created = getattr(message, "created_at", None)
        if created is None:
            return None
        if hasattr(created, "isoformat"):
            return created.isoformat()
        return str(created)
