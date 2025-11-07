from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class WorklistBase(BaseModel):
    name: str

class WorklistCreate(WorklistBase):
    pass

class WorklistRead(WorklistBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
