from datetime import datetime

from todo import Session
from todo.constants import Frequency, TaskPriorityLevel, TaskStatus
from todo.task import SubTask, SubTaskORM, Task, task_pydantic_to_orm
from todo.utils import create_date_range, get_end_of_day, get_end_of_week


def handle_add(
    description: str,
    priority: TaskPriorityLevel,
    status: TaskStatus,
    subtasks: list[str] = [],
    category: list[str] = [],
    deadline: datetime | None = None,
    eod: bool | None = None,
    eow: bool | None = None,
    schedule: Frequency | None = None,
    n_occurrences: int = 1,
):
    """Handle user using the add command."""
    if eod:
        deadline = get_end_of_day()
    elif eow:
        deadline = get_end_of_week()

    if schedule:
        if not deadline:
            raise ValueError("A deadline must be supplied for scheduling to be supported.")
        deadlines = create_date_range(
            start_datetime=deadline,
            n=n_occurrences,
            frequency=schedule,
        )
    else:
        deadlines = [deadline]
    
    for deadline in deadlines:
        _add_task(
            description=description,
            priority=priority,
            status=status,
            subtasks=subtasks,
            category=category,
            deadline=deadline,
        )

def _add_task(
    description: str,
    priority: TaskPriorityLevel,
    status: TaskStatus,
    subtasks: list[str] = [],
    category: list[str] = [],
    deadline: datetime | None = None,
) -> Task:
    """Add task."""

    task = Task(
        description=description,
        priority=priority,
        status=status,
        category=category,
        deadline=deadline,
    )
    with Session() as session:
        task_orm = task_pydantic_to_orm(task)
        session.add(task_orm)
        session.flush()
        if subtasks:
            for sub_task_id, description in enumerate(subtasks):
                sub_task = SubTask(
                    sub_task_id=sub_task_id,
                    parent_id=task_orm.task_id,
                    description=description,
                    status=TaskStatus.TODO,
                )
                sub_task_orm = SubTaskORM(
                    sub_task_id=sub_task.sub_task_id,
                    parent_id=sub_task.parent_id,
                    description=sub_task.description,
                    status=sub_task.status,
                )
                session.add(sub_task_orm)
        session.commit()