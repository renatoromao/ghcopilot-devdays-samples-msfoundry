"""Agent service backed by the Foundry SDK."""

from __future__ import annotations

from services.foundry_client import FoundryClient


class AgentService:
    def __init__(self, client: FoundryClient | None = None) -> None:
        self.client = client or FoundryClient()

    @property
    def is_configured(self) -> bool:
        return self.client.is_configured

    def status(self) -> dict:
        return self.client.status()

    def get_or_create_agent(self) -> dict:
        if not self.client.is_configured:
            return {
                "id": "local-agent",
                "name": self.client.agent_name,
                "description": self.client.agent_description,
                "model": None,
                "mode": "local",
            }

        agent = self.client.get_or_create_agent()
        agent["mode"] = "foundry"
        return agent
