import os

from google.genai import types

from functions.utils import check_if_in_workspace

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory: str, directory: str = ".") -> str:
    def get_file_info(file, target_path):
        file_with_directory = os.path.join(target_path, file)

        file_size = os.path.getsize(file_with_directory)
        is_dir = os.path.isdir(file_with_directory)
        return f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"

    # directory validation
    try:
        is_error, target_path = check_if_in_workspace(
            working_directory=working_directory, file_path=directory
        )
        if is_error:
            return f"Error: File not readable cuz its not in {working_directory}"

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        # return file info
        files_info = []

        for file in os.listdir(target_path):
            if file[0] != ".":
                files_info.append(get_file_info(file=file, target_path=target_path))
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"
