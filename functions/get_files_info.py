import os

from functions.utils import check_if_in_workspace


def get_files_info(working_directory: str, file_path: str = ".") -> str:
    def get_file_info(file, target_path):
        file_with_directory = os.path.join(target_path, file)

        file_size = os.path.getsize(file_with_directory)
        is_dir = os.path.isdir(file_with_directory)
        return f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"

    # directory validation
    try:
        is_error, target_path = check_if_in_workspace(
            working_directory=working_directory, file_path=file_path
        )
        if is_error:
            return f"Error: File not readable cuz its not in {working_directory}"

        if not os.path.isdir(target_path):
            return f'Error: "{file_path}" is not a directory'
        # return file info
        files_info = []

        for file in os.listdir(target_path):
            if file[0] != ".":
                files_info.append(get_file_info(file=file, target_path=target_path))
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"
