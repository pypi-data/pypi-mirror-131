from typing import Any, Callable

from bson import ObjectId


def processing_kwargs(func: Callable):
    """Prepares method kwargs for a query to the database.

    Args:
        func (`Callable`): Class method for querying.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        buffer = {}
        for key, value in kwargs.items():
            if key == "_id" and ObjectId.is_valid(value):
                value = ObjectId(value)
            if "__" in key:
                key, value = modifier(key, value)
            buffer[key] = value
        return func(*args, **buffer)

    return wrapper


def modifier(key: str, value: Any) -> tuple[str, dict[str, Any]]:
    """Key to modifier value.

    Args:
        key (str): Any str with `__` and modifier.
        value (Any): Any value.

    Returns:
        tuple[str, dict[str, Any]]: Key and dictionary value.
    """
    key, suffix = key.split("__")
    return (key, {"$%s" % suffix: value})
