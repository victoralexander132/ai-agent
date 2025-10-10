import os
from .path_security import is_outside_working_directory


def write_file(working_directory, file_path, content):
    try:
        if is_outside_working_directory(working_directory, file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isabs(file_path):
            joined = os.path.realpath(file_path)
        else:
            joined = os.path.realpath(os.path.join(working_directory, file_path))

        parent_dir = os.path.dirname(joined)
        
        os.makedirs(parent_dir, exist_ok=True)
        
        with open(joined, "w") as f:
            f.write(str(content))
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"
