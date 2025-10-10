import os
import subprocess
import sys
from .path_security import is_outside_working_directory


def run_python_file(working_directory, file_path, args=[]):
    try:

        if is_outside_working_directory(working_directory, file_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        abs_path = os.path.realpath(os.path.join(working_directory, file_path))

        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        list_args = [sys.executable, abs_path]
        if args:
            list_args.extend(args)
        proc = subprocess.run(
            list_args, cwd=working_directory, capture_output=True, timeout=30, text=True
        )

        parts = []
        if proc.stdout:
            parts.append(f"STDOUT: {proc.stdout.strip()}")
        if proc.stderr:
            parts.append(f"STDERR: {proc.stderr.strip()}")
        if proc.returncode != 0:
            parts.append(f"Process exited with code {proc.returncode}")
        if not parts:
            return "No output produced."
        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
