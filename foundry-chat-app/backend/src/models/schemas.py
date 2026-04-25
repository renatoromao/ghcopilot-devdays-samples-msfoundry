from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    sender: str
    content: str
    timestamp: str

class ChatSchema(BaseModel):
    messages: List[Message]
    agent_id: str
    user_id: Optional[str] = None

class AgentSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: str
    updated_at: str