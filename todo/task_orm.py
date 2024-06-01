from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry
from datetime import datetime
from datetime import datetime
from pydantic import BaseModel
from todo.constants import TaskPriorityLevel, TaskStatus
from todo import engine

class Task(BaseModel):
    """Base task class."""
    task_id: int | None = None
    description: str
    priority: TaskPriorityLevel
    status: TaskStatus
    categories: list[str] = []
    creation_datetime: datetime = datetime.now()
    deadline: datetime | None = None
    completion_datetime: datetime | None = None


class SubTask(BaseModel):
    """Subtask class."""
    task_id: int | None = None
    parent: Task
    description: str
    status: TaskStatus
    next_sub_task: SubTask | None
    previous_sub_task: SubTask | None

Base = declarative_base()
mapper_registry = registry()

class TaskORM(Base):
    """ORM model for tasks."""
    __tablename__ = 'tasks'
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    priority = Column(String)  # Assuming TaskPriorityLevel is a string enum
    status = Column(String)  # Assuming TaskStatus is a string enum
    categories = Column(String)  # Assuming categories will be stored as comma-separated values
    creation_datetime = Column(DateTime, default=datetime.now)
    deadline = Column(DateTime, nullable=True)
    completion_datetime = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)


def orm_to_pydantic(task_orm: TaskORM) -> Task:
    """Convert task ORM object to task pydantic instance."""
    return Task(
        task_id=task_orm.task_id,
        description=task_orm.description,
        priority=task_orm.priority,
        status=task_orm.status,
        categories=task_orm.categories.split(',') if task_orm.categories else [],
        creation_datetime=task_orm.creation_datetime,
        deadline=task_orm.deadline,
        completion_datetime=task_orm.completion_datetime
    )

def pydantic_to_orm(task: Task, clone_id: bool = False) -> TaskORM:
    """Convert task pydantic instance to ORM"""
    task_orm = TaskORM(
        description=task.description,
        priority=task.priority,
        status=task.status,
        categories=','.join(task.categories),
        creation_datetime=task.creation_datetime,
        deadline=task.deadline,
        completion_datetime=task.completion_datetime
    )
    if clone_id:
        task_orm.task_id = task.task_id
    return task_orm