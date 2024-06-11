

from argparse import Namespace

from todo import Session
from todo.task import SubTaskORM, TaskORM


def handle_remove(tasks: list[int]):
    """Handle user using the remove command."""
    with Session() as session:
        session.query(SubTaskORM).filter(
            SubTaskORM.parent_id.in_(tasks)
        ).delete()
        
        session.query(TaskORM).filter(
            TaskORM.task_id.in_(tasks)
        ).delete()
        session.commit()