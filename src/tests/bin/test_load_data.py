from typing import Any

from pytest import fixture

from bin.load_data import do_load_files
from bin.load_data import find_users


def test_do_load_files() -> None:
    data = do_load_files()
    assert isinstance(data, list)
    assert len(data) == 96
    for d in data:
        assert isinstance(d, dict)
        for k in d:
            assert isinstance(k, str)


@fixture
def file_data() -> list[dict[str, Any]]:
    return do_load_files()


def test_find_users(file_data: list[dict[str, Any]]) -> None:
    users = find_users(file_data)
    assert isinstance(users, dict)
    assert len(users) == 84
    for k, v in users.items():
        assert isinstance(k, str)
        assert isinstance(v, str)
