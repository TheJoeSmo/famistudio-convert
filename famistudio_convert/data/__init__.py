from importlib.resources import read_text as _read_text


def read_text(path: str) -> str:
    return _read_text(__package__, path)
