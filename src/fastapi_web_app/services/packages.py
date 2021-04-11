def package_count() -> int:
    return 274000


def release_count() -> int:
    return 2234847


def latest_packages(*, limit: int = 5) -> list[dict[str, str]]:
    return [{"id": "fastapi", "summary": "What you want to master"}][:limit]
