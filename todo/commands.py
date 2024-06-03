from argparse import Namespace
from sqlalchemy.sql.expression import nullslast
from todo import Session
from todo.constants import TaskPriorityLevel, TaskStatus
from todo.task_orm import Task, TaskORM, orm_to_pydantic, pydantic_to_orm
from todo.utils import get_end_of_day, get_end_of_week, get_pretty_tasks, is_current_day, is_current_week, is_task_overdue

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

def handle_update(args: Namespace):
    """Handle user using the update command."""
    if args.today:
        args.deadline = get_end_of_day()
    elif args.week:
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
            task = orm_to_pydantic(task_orm)
            for field_name, new_value in field_args.items():
                setattr(task, field_name, new_value)
            updated_task_orm = pydantic_to_orm(task, clone_id=True)
            for field_name in field_args:
                setattr(task_orm, field_name, getattr(updated_task_orm, field_name))
            session.add(task_orm)
            print(f"task {task.task_id} updated")
        session.commit()


def handle_list(args: Namespace):
    """Handle user using the list command."""
    status_filter = args.status or list(TaskStatus)
    priority_filter = args.priority or list(TaskPriorityLevel)

    with Session() as session:
        result = session.query(TaskORM).filter(
            TaskORM.status.in_(status_filter),
            TaskORM.priority.in_(priority_filter)
        ).order_by(
            nullslast(TaskORM.deadline.asc()),
            TaskORM.priority.desc(),
        )
        tasks = [
            orm_to_pydantic(task) for task in result
        ]
    if args.category:
        tasks = [task for task in tasks if set(task.category) & set(args.category)]
    if args.week:
        tasks = [
            task for task in tasks 
            if task.deadline 
            and (is_current_week(task.deadline) or is_task_overdue(task))
        ]
    if args.today:
        tasks = [task for task in tasks if task.deadline and (is_current_day(task.deadline) or is_task_overdue(task))]
    if tasks:
        print(get_pretty_tasks(tasks))
    else:
        print("No tasks found.")

def handle_remove(args: Namespace):
    """Handle user using the remove command."""
    with Session() as session:
        session.query(TaskORM).filter(
            TaskORM.task_id.in_(args.tasks)
        ).delete()
        session.commit()

def handle_sync(args: Namespace):
    """Handle user using the sync command."""
    from todo import git_utils
    if args.init_repository:
        git_utils.clone(args.init_repository)
    if args.pull:
        git_utils.pull()
        git_utils.copy_git_db_to_local_folder()
    if args.push:
        git_utils.pull()
        git_utils.copy_local_db_to_git_repo()
        git_utils.push()