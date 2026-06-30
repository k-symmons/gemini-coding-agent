import os

from google.genai import types

from functions.utils import check_if_in_workspace

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file specifed in working directory. Returns str depending on result",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="Text content to write to the file"
            ),
        },
        required=["file_path", "content"],
    ),
)


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
