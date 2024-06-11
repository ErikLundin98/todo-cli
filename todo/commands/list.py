

from argparse import Namespace
from sqlalchemy.sql.expression import nullslast

from todo import Session
from todo.constants import TaskPriorityLevel, TaskStatus
from todo.task import TaskORM, task_orm_to_pydantic
from todo.utils import get_pretty_tasks, is_current_day, is_current_week, is_task_overdue


def handle_list(
    status: list[TaskStatus] | None = None,
    priority: list[TaskPriorityLevel] | None = None,
    category: list[str] = [],
    week: bool | None = None,
    today: bool | None = None,
):
    """Handle user using the list command."""
    status_filter = status or list(TaskStatus)
    priority_filter = priority or list(TaskPriorityLevel)

    with Session() as session:
        result = session.query(TaskORM).filter(
            TaskORM.status.in_(status_filter),
            TaskORM.priority.in_(priority_filter)
        ).order_by(
            nullslast(TaskORM.deadline.asc()),
            TaskORM.priority.desc(),
        )
        tasks = [
            task_orm_to_pydantic(task) for task in result
        ]
    if category:
        tasks = [task for task in tasks if set(task.category) & set(category)]
    if week:
        tasks = [
            task for task in tasks 
            if task.deadline 
            and (is_current_week(task.deadline) or is_task_overdue(task))
        ]
    if today:
        tasks = [task for task in tasks if task.deadline and (is_current_day(task.deadline) or is_task_overdue(task))]
    if tasks:
        print(get_pretty_tasks(tasks))
    else:
        print("No tasks found.")