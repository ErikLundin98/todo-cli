import argparse

from todo.constants import EXPECTED_DATETIME_FORMAT, EXPECTED_DATETIME_FORMAT_STRING, TaskPriorityLevel, TaskStatus
from todo.commands import handle_add, handle_list, handle_remove, handle_sync, handle_update
from todo.utils import parse_datetime

parser = argparse.ArgumentParser(
    prog="todo",
    description="Helps you to organize your TODO:s, reminders etc.",
    epilog="Try todo -h for getting help!"
)

subparsers = parser.add_subparsers(title="sub-commands", dest="command")

parser_add = subparsers.add_parser("add", aliases=["a"], help="Add a new task")
parser_add.add_argument("description", type=str, help="Description to set for task")
parser_add.add_argument('--today', action="store_true", help='Shorthand argument for setting deadline to EOD today')
parser_add.add_argument('--week', action="store_true", help='Shorthand argument for setting deadline to EOW')
parser_add.add_argument("-i", "--priority", type=TaskPriorityLevel, required=False, default=TaskPriorityLevel.LOW, help=f"Priority to set for task ({list(TaskPriorityLevel)}). Defaults to low")
parser_add.add_argument("-s", "--status", type=TaskStatus, required=False, default=TaskStatus.TODO, help=f"Status to set for task ({list(TaskStatus)}). Defaults to todo")
parser_add.add_argument("-c", "--category", type=str, nargs="+", required=False, default=[], help="Category/Categories to set for task")
parser_add.add_argument("-dl", "--deadline", type=parse_datetime, required=False, default=None, help=f"Optional due date of the task (format: {EXPECTED_DATETIME_FORMAT_STRING}). Time is optional, and will default to EOD.")

parser_update = subparsers.add_parser("update", aliases=["u"], help="Update a task")
parser_update.add_argument("task", type=int, nargs="+", help="ID of the task(s) to update")
parser_update.add_argument('--today', action="store_true", help='Shorthand argument for setting deadline to EOD today')
parser_update.add_argument('--week', action="store_true", help='Shorthand argument for setting deadline to EOW')
parser_update.add_argument('--done', action="store_true", help='Shorthand argument for marking task(s) as done')
parser_update.add_argument('--in-progress', action="store_true", help='Shorthand argument for marking task(s) as in progress')
parser_update.add_argument('--todo', action="store_true", help='Shorthand argument for marking task(s) as TODO')



parser_update.add_argument("-d", "--description", type=str, required=False, help=f"Description to set for task ({list(TaskStatus)})")
parser_update.add_argument("-i", "--priority", type=TaskPriorityLevel, required=False, help=f"Priority to set for task ({list(TaskPriorityLevel)})")
parser_update.add_argument("-s", "--status", type=TaskStatus, required=False, help="Status to set for task")
parser_update.add_argument("-c", "--category", type=str, nargs="+", required=False, help="Category/Categories to set for task")
parser_update.add_argument("-dl", "--deadline", type=parse_datetime, required=False, help=f"Due date of the task (format: {EXPECTED_DATETIME_FORMAT_STRING}). Time is optional, and will default to EOD.")

parser_list = subparsers.add_parser("list", aliases=["ls"], help="List tasks.")
parser_list.add_argument('--today', action="store_true", help='Filter on actions due today (or overdue)')
parser_list.add_argument('--week', action="store_true", help='Filter on actions due this week (or overdue)')
parser_list.add_argument("-s", "--status", type=TaskStatus, nargs="+", required=False, default=list(TaskStatus), help="Status level to filter for")
parser_list.add_argument("-i", "--priority", type=TaskPriorityLevel, nargs="+", required=False, default=list(TaskPriorityLevel), help="Priority level to filter for")
parser_list.add_argument("-c", "--category", type=str, nargs="+", required=False, help="Category/categories to filter for")


parser_list = subparsers.add_parser("remove", aliases=["rm"], help="Remove tasks completely.")
parser_list.add_argument("tasks", type=str, nargs="+", help="Task id(s) to remove.")

parser_sync = subparsers.add_parser("sync", aliases=["s"], help="Sync data using git.")
parser_sync.add_argument("-i", "--init-repository", type=str, required=False, help='Initialize git syncing by cloning a remote repository. SSH keys or other auth method must be setup beforehand.')
parser_sync.add_argument('--pull', action="store_true", help='Overwrite local db with what is in remote git repository')
parser_sync.add_argument('--push', action="store_true", help='Overwrite remote git repository with what is in local db')


args = parser.parse_args()
match args.command:
    case "add":
        handle_add(args)
    case "update":
        handle_update(args)
    case "list":
        handle_list(args)
    case "remove":
        handle_remove(args)
    case "sync":
        handle_sync(args)
    case _:
        print("could not recognize the given command.")