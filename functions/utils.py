import os


def check_if_in_workspace(working_directory: str, file_path: str = "."):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    if os.path.commonpath([abs_working_dir, target_path]) != abs_working_dir:
        return (True, target_path)

    return (False, target_path)
