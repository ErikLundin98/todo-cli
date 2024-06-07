

from argparse import Namespace

from todo import Session
from todo.task import TaskORM


def handle_remove(args: Namespace):
    """Handle user using the remove command."""
    with Session() as session:
        session.query(TaskORM).filter(
            TaskORM.task_id.in_(args.tasks)
        ).delete()
        session.commit()