import os
import subprocess

from functions.utils import check_if_in_workspace


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # checks
        is_error, target_path = check_if_in_workspace(
            working_directory=working_directory, file_path=file_path
        )
        if is_error:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, timeout=30, text=True)

        output_str = ""

        # negative return code means it failed
        if result.returncode != 0:
            output_str += f"Process exited with code {result.returncode} \n"

        if not result.stderr and not result.stdout:
            output_str += "No output produced\n"
        else:
            output_str += f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}\n"

        return output_str

    except Exception as e:
        return f"Error: executing python file: {e}"
