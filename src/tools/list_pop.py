__all__ = ["safe_pop"]


def safe_pop(data: list):
    return data.pop() if data else None
