import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.realpath(full_path)

        if not full_path.startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

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
