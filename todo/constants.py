from enum import IntEnum, StrEnum, auto
from pathlib import Path
DB_DIRNAME = "db"
DATA_DIRNAME = "data"
GIT_DIRNAME = "git"
DB_NAME = "tasks.db"
DATA_DIR =  Path(__file__).parent.parent.resolve() / DATA_DIRNAME
DB_DIR = DATA_DIR / DB_DIRNAME 
DB_PATH = DB_DIR / DB_NAME
GIT_REPO_DIR = DATA_DIR / GIT_DIRNAME
GIT_REPO_URL = "GIT_REPO_URL"

EXPECTED_DATE_FORMAT = "%Y-%m-%d"
EXPECTED_TIME_FORMAT = "%H:%M"
EXPECTED_DATETIME_FORMAT = EXPECTED_DATE_FORMAT + " " + EXPECTED_TIME_FORMAT
EXPECTED_DATETIME_FORMAT_STRING = "YYYY-MM-DD HH:MM:SS"


class TaskPriorityLevel(IntEnum):
    """Level of priority for tasks."""
    LOWEST = 5
    LOW = 4
    MEDIUM = 3
    HIGH = 2
    HIGHEST = 1

class TaskStatus(StrEnum):
    """Status for task."""
    TODO = auto()
    IN_PROGRESS = auto()
    DONE = auto()

class CommandLineColor(StrEnum):
    """ANSI escape codes for colors."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[33m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'