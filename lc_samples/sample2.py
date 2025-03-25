from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class Recipe(BaseModel):
    ingredients: list[str] = Field(..., description="The ingredients for the recipe")
    steps: list[str] = Field(description="The name of the recipe")


def main():
    output_parser = PydanticOutputParser(pydantic_object=Recipe)

    format_instructions = output_parser.get_format_instructions()
    print(format_instructions)

    """
    The output should be formatted as a JSON instance that conforms to the JSON schema below.

    As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
    the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.
    
    Here is the output schema:
    ```
    {"properties": {"ingredients": {"description": "The ingredients for the recipe", "items": {"type": "string"}, "title": "Ingredients", "type": "array"}, "steps": {"description": "The name of the recipe", "items": {"type": "string"}, "title": "Steps", "type": "array"}}, "required": ["ingredients", "steps"]}
    ```
    """


if __name__ == "__main__":
    main()
