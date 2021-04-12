def try_int(text: str) -> int:
    try:
        return int(text)
    except (ValueError, TypeError):
        return 0
