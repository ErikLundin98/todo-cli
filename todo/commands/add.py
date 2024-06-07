from argparse import Namespace

from todo import Session
from todo.constants import TaskStatus
from todo.task import SubTask, SubTaskORM, Task, task_pydantic_to_orm
from todo.utils import get_end_of_day, get_end_of_week


def handle_add(args: Namespace):
    """Handle user using the add command."""
    if args.today:
        deadline = get_end_of_day()
    elif args.week:
        deadline = get_end_of_week()
    else:
        deadline = args.deadline
    task = Task(
        description=args.description,
        priority=args.priority,
        status=args.status,
        category=args.category,
        deadline=deadline,
    )
    with Session() as session:
        task_orm = task_pydantic_to_orm(task)
        session.add(task_orm)
        session.flush()
        if args.subtasks:
            for sub_task_id, description in enumerate(args.subtasks):
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