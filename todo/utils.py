import argparse
from datetime import datetime, time, timedelta
import calendar

from emoji import emojize
from tabulate import tabulate
from todo import Session
from todo.constants import EXPECTED_DATETIME_FORMAT, CommandLineColor, Frequency, TaskPriorityLevel, TaskStatus
from todo.task import SubTask, SubTaskORM, Task


class ParseKeyValuePairs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        kv_dict = {}
        for value in values:
            key, val = value.split('=', 1)
            kv_dict[key] = val
        setattr(namespace, self.dest, kv_dict)
        
def parse_task_priority_level(arg: str) -> TaskPriorityLevel:
    return TaskPriorityLevel(int(arg))

def parse_datetime(arg: str) -> datetime:
    if " " not in arg: # Assume no time is passed.
        datetime_str = f"{arg} 23:59"
    else:
        datetime_str = arg

    return datetime.strptime(datetime_str, EXPECTED_DATETIME_FORMAT)

def is_current_week(timestamp: datetime) -> bool:
    """Return whether datetime is during current week."""
    return get_start_of_week() <= timestamp <= get_end_of_week()

def get_start_of_week() -> datetime:
    """Get start of week as datetime."""
    today = get_beginning_of_day()
    return today - timedelta(days=today.weekday())

def get_end_of_week() -> datetime:
    """Get end of week as datetime."""
    return get_start_of_week() + timedelta(days=6)

def get_beginning_of_day() -> datetime:
    """Get beginning of day as datetime."""
    today = datetime.now()
    return datetime.combine(today.date(), time(hour=0, minute=0))

def get_end_of_day() -> datetime:
    """Get end of day as datetime."""
    today = datetime.now()
    return datetime.combine(today.date(), time(hour=23, minute=59))

def is_current_day(timestamp: datetime) -> bool:
    """Return whether datetime is current day."""
    return timestamp.date() == datetime.now().date()

def is_task_overdue(task: Task) -> bool:
    """Return whether task is overdue or not."""
    return task.deadline and datetime.now() > task.deadline and task.status != TaskStatus.DONE

def get_pretty_tasks(tasks: list[Task]):
    """Pretty table representation of list of tasks."""
    table = []
    headers = [
        "ID",
        "description",
        "priority",
        "status",
        "category",
        "deadline",
        "message",
    ]
    for task in tasks:
        if is_task_overdue(task):
            message = color_text("Overdue!", CommandLineColor.RED) + emojize(":hot_face:")
        elif task.status == TaskStatus.DONE:
            message = color_text("All done.", CommandLineColor.GREEN) + emojize(":check_mark_button:")
        elif task.status == TaskStatus.IN_PROGRESS:
            message = color_text("Keep grinding king.", CommandLineColor.CYAN) + emojize(":crown:")
        elif task.status == TaskStatus.TODO and task.deadline and task.deadline <= datetime.today() + timedelta(hours=24):
            message = color_text("Time to start this one.", CommandLineColor.BRIGHT_RED) + emojize(":alarm_clock:")
        elif task.status == TaskStatus.TODO and task.deadline and task.deadline <= get_end_of_week():
            message = color_text("Are you on top of this?", CommandLineColor.YELLOW) + emojize(":spiral_calendar:")
        else:
            message = "No rush." + emojize(":sloth:")
        if task.status == TaskStatus.DONE:
            description = color_text(task.description, CommandLineColor.STRIKETHROUGH)
        else:
            description = task.description
        table_data = [
            task.task_id,
            description,
            task.priority,
            task.status,
            task.category,
            task.deadline,
            message,
        ]
        subtasks = get_subtasks(task.task_id)
        if len(subtasks):
            table_data = [color_text(text, CommandLineColor.UNDERLINE) for text in table_data]
        
        table += [table_data]
        for subtask in subtasks:
            if subtask.status == TaskStatus.DONE:
                description = color_text(subtask.description, CommandLineColor.STRIKETHROUGH)
            else:
                description = subtask.description
            table += [[
                emojize(":left_arrow_curving_right:") + f"{subtask.parent_id}.{subtask.sub_task_id}",
                description,
                "",
                subtask.status,
                "",
                "",
                "",
            ]]

    return tabulate(
        tabular_data=table,
        headers=headers,
        tablefmt="rounded_grid",
    )

def create_date_range(start_datetime: datetime, n: int, frequency: Frequency) -> list[datetime]:
    """Create date range from start datetime, n occurrences and frequency"""
    match frequency:
        case Frequency.DAILY:
            delta_fn = lambda date_time: date_time + timedelta(days=1)
        case Frequency.WEEKDAYS:
            delta_fn = lambda date_time: date_time + timedelta(days=1) if date_time.weekday() <= 3 else date_time + timedelta(days=3)
        case Frequency.WEEKLY:
            delta_fn = lambda date_time: date_time + timedelta(weeks=1)
        case Frequency.MONTHLY:
            delta_fn = lambda date_time: date_time + timedelta(
                days=calendar.monthrange(date_time.year, date_time.month)[1]
            )
        case Frequency.YEARLY:
            delta_fn = lambda date_time: datetime(
                year=date_time.year + 1,
                month=date_time.month,
                day=date_time.day,
                hour=date_time.hour,
                minute=date_time.minute,
                second=date_time.second,
            )
    
    date_range = [start_datetime]
    current_datetime = start_datetime
    for _ in range(n-1):
        current_datetime = delta_fn(current_datetime)
        date_range.append(current_datetime)

    return date_range

def color_text(text: str, color_ansi: CommandLineColor | list[CommandLineColor]):
    """Utility function to create string that will render in specific color in command line."""
    if isinstance(color_ansi, list):
        color_ansi = "".join(color_ansi)
    return f"{color_ansi}{text}{CommandLineColor.RESET_ALL_ATTRIBUTES}"

def get_subtasks(task_id: int) -> list[SubTask]:
    """Get all subtasks associated with a subtask."""
    with Session() as session:
        result = session.query(SubTaskORM).filter(
            SubTaskORM.parent_id == task_id,
        ).order_by(SubTaskORM.sub_task_id)

        if not result:
            sub_tasks = []
        else:
            sub_tasks = [
                SubTask(
                    sub_task_id=sub_task_orm.sub_task_id,
                    parent_id=sub_task_orm.parent_id,
                    description=sub_task_orm.description,
                    status=sub_task_orm.status,
                )
                for sub_task_orm in result
            ]
    return sub_tasks