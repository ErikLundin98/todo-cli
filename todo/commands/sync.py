from argparse import Namespace


def handle_sync(
    init_repository: str | None = None,
    pull: bool | None = None,
    push: bool | None = None,
):
    """Handle user using the sync command."""
    from todo import git_utils
    if init_repository:
        git_utils.clone(init_repository)
    if pull:
        git_utils.pull()
        git_utils.copy_git_db_to_local_folder()
    if push:
        git_utils.pull()
        git_utils.copy_local_db_to_git_repo()
        git_utils.push()