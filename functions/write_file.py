import os

from functions.utils import check_if_in_workspace


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        is_error, target_path = check_if_in_workspace(
            working_directory=working_directory, file_path=file_path
        )
        if is_error:
            raise Exception(
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )
        if os.path.isdir(target_path):
            raise Exception(
                f'Error: Cannot write to "{file_path}" as it is a directory'
            )

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        open(target_path, mode="w").write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error:{e}"
