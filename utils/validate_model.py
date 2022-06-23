from typing import List, Any


def validate_model(object: Any, fields: List[str]) -> bool:
    """
    Validate if the given Object has all the fields

    Arguments:
        object: Object which needs to validated
        fields: field names which the object needs to contain

    Raises:
        AttributeError: If the object does not contain a given field

    Returns:
        Boolean: True if all the fields exists
    """

    for field in fields:
        if not hasattr(object, field):
            raise AttributeError(f"{type(object)} has not attribute {field}")

    return True
