from datetime import datetime
from git import Repo
import shutil
from pathlib import Path

from todo.constants import DB_NAME, DB_PATH, GIT_REPO_DIR


def clone(url: str):
    Repo.clone_from(url, GIT_REPO_DIR)
    print(f"Successfully cloned remote repository {url}")

def pull():
    print("Pulling latest changes from remote git repository")
    repo = Repo(GIT_REPO_DIR)
    origin = repo.remotes.origin
    origin.pull()
    print("Pull complete")

def push():
    print("Pushing latest data from repository")
    repo = Repo(GIT_REPO_DIR)
    repo.git.add(A=True)
    repo.index.commit(f"DB sync {datetime.now()}")
    origin = repo.remotes.origin
    origin.push()
    print("Push complete")

def copy_local_db_to_git_repo():
    if DB_PATH.exists():
        shutil.copy(
            DB_PATH,
            GIT_REPO_DIR / DB_NAME,
        )  
        print("Overwrote git data with local data.")
    else:
        print("Could not find local db. Have you set up everything correctly?")

def copy_git_db_to_local_folder():
    if Path(GIT_REPO_DIR, DB_NAME).exists():
        shutil.copy(
            GIT_REPO_DIR / DB_NAME,
            DB_PATH,
        )
        print("Overwrote local data with git data.")
    else:
        print("Could not find git db. Have you set up everything correctly?")