

from argparse import Namespace

from todo import Session
from todo.constants import TaskStatus
from todo.task import SubTaskORM, Task, TaskORM, task_orm_to_pydantic, task_pydantic_to_orm
from todo.utils import get_end_of_day, get_end_of_week


def handle_update(args: Namespace):
    """Handle user using the update command."""
    if args.eod:
        args.deadline = get_end_of_day()
    elif args.eow:
        args.deadline = get_end_of_week()
    if args.done:
        args.status = TaskStatus.DONE
    elif args.in_progress:
        args.status = TaskStatus.IN_PROGRESS
    elif args.todo:
        args.status = TaskStatus.TODO
    field_args = {k: v for k, v in vars(args).items() if k in Task.__fields__ and v is not None}
    with Session() as session:
        session.begin()
        task_ids = args.task
        result = session.query(TaskORM).filter(
            TaskORM.task_id.in_(task_ids)
        ).all()

       
        for task_orm in result:
            for sub_task_id, status in (args.subtasks or {}).items():
                sub_task: SubTaskORM = session.query(SubTaskORM).filter(
                    SubTaskORM.parent_id == task_orm.task_id,
                    SubTaskORM.sub_task_id == int(sub_task_id)
                ).one()
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