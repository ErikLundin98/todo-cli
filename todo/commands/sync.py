from argparse import Namespace


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