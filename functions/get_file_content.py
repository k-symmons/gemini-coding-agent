import os

from config import MAX_CHARS
from functions.utils import check_if_in_workspace


def get_file_content(working_directory: str, file_path: str):
    try:
        is_error, target_path = check_if_in_workspace(
            working_directory=working_directory, file_path=file_path
        )
        if is_error:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # todo: add support for filetype other than text
        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content
    except Exception as e:
        return f"Error: {e}"
