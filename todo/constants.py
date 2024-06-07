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
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background Colors
    BACKGROUND_BLACK = '\033[40m'
    BACKGROUND_RED = '\033[41m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_YELLOW = '\033[43m'
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_MAGENTA = '\033[45m'
    BACKGROUND_CYAN = '\033[46m'
    BACKGROUND_WHITE = '\033[47m'
    BACKGROUND_BRIGHT_BLACK = '\033[100m'
    BACKGROUND_BRIGHT_RED = '\033[101m'
    BACKGROUND_BRIGHT_GREEN = '\033[102m'
    BACKGROUND_BRIGHT_YELLOW = '\033[103m'
    BACKGROUND_BRIGHT_BLUE = '\033[104m'
    BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
    BACKGROUND_BRIGHT_CYAN = '\033[106m'
    BACKGROUND_BRIGHT_WHITE = '\033[107m'

    # Text Attributes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    RAPID_BLINK = '\033[6m'
    INVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    RESET_ALL_ATTRIBUTES = '\033[0m'
    RESET_BOLD = '\033[21m'
    RESET_DIM = '\033[22m'
    RESET_ITALIC = '\033[23m'
    RESET_UNDERLINE = '\033[24m'
    RESET_BLINK = '\033[25m'
    RESET_HIDDEN = '\033[28m'
    RESET_STRIKETHROUGH = '\033[29m'