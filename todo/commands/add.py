from argparse import Namespace

from todo import Session
from todo.task_orm import Task, pydantic_to_orm
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
        task_orm = pydantic_to_orm(task)
        session.add(task_orm)
        session.commit()