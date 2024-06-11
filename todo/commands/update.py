from argparse import Namespace
from datetime import datetime

from todo import Session
from todo.constants import TaskPriorityLevel, TaskStatus
from todo.task import (
    SubTaskORM,
    TaskORM,
    task_orm_to_pydantic,
    task_pydantic_to_orm,
)
from todo.utils import get_end_of_day, get_end_of_week


def handle_update(
    task: list[int] = None,
    description: str | None = None,
    priority: TaskPriorityLevel | None = None,
    category: list[str] | None = None,
    eod: bool | None = None,
    eow: bool | None = None,
    deadline: datetime | None = None,
    done: bool | None = None,
    todo: bool | None = None,
    in_progress: bool | None = None,
    status: TaskStatus | None = None,
    subtasks: dict[int, TaskStatus] = {},
):
    """Handle user using the update command."""
    if eod:
        deadline = get_end_of_day()
    elif eow:
        deadline = get_end_of_week()
    if done:
        status = TaskStatus.DONE
    elif in_progress:
        status = TaskStatus.IN_PROGRESS
    elif todo:
        status = TaskStatus.TODO

    field_args = {
        field: value
        for field, value in {
            "description": description,
            "priority": priority,
            "status": status,
            "category": category,
            "deadline": deadline,
        }.items()
        if value is not None
    }
    with Session() as session:
        session.begin()
        task_ids = task
        result = session.query(TaskORM).filter(TaskORM.task_id.in_(task_ids)).all()

        for task_orm in result:
            for sub_task_id, status in (subtasks or {}).items():
                sub_task: SubTaskORM = (
                    session.query(SubTaskORM)
                    .filter(
                        SubTaskORM.parent_id == task_orm.task_id,
                        SubTaskORM.sub_task_id == int(sub_task_id),
                    )
                    .one()
                )
                sub_task.status = TaskStatus(status)
            task = task_orm_to_pydantic(task_orm)
            for field_name, new_value in field_args.items():
                setattr(task, field_name, new_value)
            updated_task_orm = task_pydantic_to_orm(task, clone_id=True)
            for field_name in field_args:
                setattr(task_orm, field_name, getattr(updated_task_orm, field_name))
            session.add(task_orm)
            print(f"task {task.task_id} updated")
        session.commit()
