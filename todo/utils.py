from datetime import datetime, time, timedelta

from emoji import emojize
from tabulate import tabulate
from todo.constants import EXPECTED_DATETIME_FORMAT, CommandLineColor, TaskPriorityLevel, TaskStatus
from todo.task_orm import Task

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
    today = get_end_of_day()
    return today - timedelta(days=today.weekday())

def get_end_of_week() -> datetime:
    """Get end of week as datetime."""
    return get_start_of_week() + timedelta(days=6)

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
            message = color_text("Time to start this one.", CommandLineColor.ORANGE) + emojize(":alarm_clock:")
        elif task.status == TaskStatus.TODO and task.deadline and task.deadline <= get_end_of_week():
            message = color_text("Are you on top of this?", CommandLineColor.YELLOW) + emojize(":spiral_calendar:")
        else:
            message = "No rush." + emojize(":sloth:")
        table += [[
            task.task_id,
            task.description,
            task.priority,
            task.status,
            task.category,
            task.deadline,
            message,
        ]]
    return tabulate(
        tabular_data=table,
        headers=headers,
        tablefmt="rst",
    )


def color_text(text: str, color_ansi: CommandLineColor):
    """Utility function to create string that will render in specific color in command line."""
    return f"{color_ansi}{text}{CommandLineColor.RESET}"