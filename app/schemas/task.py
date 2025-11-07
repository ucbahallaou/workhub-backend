from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class TaskBase(BaseModel):
    title: str
    status: str = "todo"  # todo | in_progress | done

class TaskCreate(TaskBase):
    worklist_id: UUID
    assignee_id: UUID | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    status: str | None = None
    assignee_id: UUID | None = None

class TaskRead(TaskBase):
    id: UUID
    worklist_id: UUID
    assignee_id: UUID | None
    created_at: datetime
    updated_at: datetime
