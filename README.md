# TODO-cli

This repo contains the TODO CLI I use on a daily basis to manage tasks.
The functionality is currently limited to the following:

- Add, list, update & delete TODO:s
- Sync todo:s using git

## Backlog

- Add support for subtasks
- LLM support to ease task creation
- Some clever way to integrate with mobile devices
- Auto sync on updates
- Automatic reminders
- Clean up code

## Installation

Using pypi: Not yet supported

Requires python to be installed (developed using Python 3.11)

```bash
git clone https://github.com/ErikLundin98/todo-cli
cd todo-cli
make install_cli
```

## Usage examples

List todos:

`todo --help`: Get some help :)

`todo list`: List all TODO:s

`todo list --today`: List all TODO:s due today

`todo add "Help with the dishes" --priority 1 --category home cleaning --today`: Create TODO that needs to be done today with top priority and category "home" and "cleaning"

TODO:s are stored and managed in a sqlite database. As a hacky cross-device sync solution, you can synchronize the database using a git repo:

`todo sync --init-repository <repo_url>`: Clone a remote git repository to use for version handling the database

`todo sync --pull`: Pull latest changes from the repo, and overwrite local database data with what is in remote

`todo sync --push`: Push local database data to remote