from pydantic import BaseModel, ConfigDict
import re


def to_camel(string: str) -> str:
    """
    Converts a snake_case string to camelCase.

    Args:
        string (str): The input string in snake_case format.

    Returns:
        str: The converted string in camelCase format.

    Example:
        >>> to_camel("example_string")
        'exampleString'
    """
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelCaseModel(BaseModel):
    """
    A Pydantic BaseModel subclass that automatically converts field names
    from snake_case to camelCase when serializing to JSON.

    Attributes:
        model_config (ConfigDict): Configuration for the Pydantic model.
            - alias_generator: A function (`to_camel`) that generates camelCase aliases for field names.
            - populate_by_name: Allows population of fields by their original names (snake_case) or aliases (camelCase).

    Usage:
        Use this class as a base for your Pydantic models to ensure camelCase serialization.

    Example:
        class ExampleModel(CamelCaseModel):
            example_field: str

        model = ExampleModel(example_field="value")
        print(model.model_dump(by_alias=True))  # Output: {"exampleField": "value"}
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
