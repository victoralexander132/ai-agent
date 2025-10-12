import os
from google.genai import types
from config import MAX_CHARS
from .path_security import is_outside_working_directory


def get_file_content(working_directory, file_path):
    try:
        if is_outside_working_directory(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.realpath(full_path)

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > 0:
                return (
                    file_content_string
                    + f'[... File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return file_content_string

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content of the file provided within working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get content from, relative to the working directory.",
            ),
        },
    ),
)
