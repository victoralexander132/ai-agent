import os
from .path_security import is_outside_working_directory


def get_files_info(working_directory, directory="."):
    try:
        if is_outside_working_directory(working_directory, directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        full_path = os.path.join(working_directory, directory)
        abs_full_path = os.path.abspath(full_path)

        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        dir_content = os.listdir(abs_full_path)
        content_summary = []
        for item in dir_content:
            item_path = os.path.join(abs_full_path, item)
            is_dir = os.path.isdir(item_path)
            item_size = os.path.getsize(item_path)
            content_summary.append(
                f"- {item}: file_size={item_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(content_summary)
    except Exception as e:
        return f"Error: {e}"
