from pathlib import Path

from git import Repo


def get_db_path() -> Path:
    root = Path(Repo(".", search_parent_directories=True).working_tree_dir)
    return root.joinpath("db", "pypi.sqlite")
