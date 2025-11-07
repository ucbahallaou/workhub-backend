# app/db/models.py
import uuid
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

RoleEnum = Enum("admin", "user", name="role_enum")
TaskStatusEnum = Enum("todo", "in_progress", "done", name="task_status_enum")

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(RoleEnum, default="user", nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    worklists: Mapped[list["Worklist"]] = relationship(back_populates="owner", cascade="all,delete")
    tasks_assigned: Mapped[list["Task"]] = relationship(back_populates="assignee", foreign_keys="Task.assignee_id")

class Worklist(Base):
    __tablename__ = "worklists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    owner: Mapped["User"] = relationship(back_populates="worklists")
    tasks: Mapped[list["Task"]] = relationship(back_populates="worklist", cascade="all,delete")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    worklist_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("worklists.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(TaskStatusEnum, default="todo", nullable=False)
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    worklist: Mapped["Worklist"] = relationship(back_populates="tasks")
    assignee: Mapped["User | None"] = relationship(back_populates="tasks_assigned", foreign_keys=[assignee_id])
