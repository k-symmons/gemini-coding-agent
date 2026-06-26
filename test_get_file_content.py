from functions.get_file_content import get_file_content


def test_get_file_content(directory: str, file_dir: str):
    try:
        result = get_file_content(directory, file_dir)

        print(f"{file_dir} length: {len(result)}")
        print(f"{file_dir} truncated: {'truncated' in result}")
        print(str(result))
    except Exception as e:
        print(e)


test_get_file_content("calculator", "lorem.txt")
test_get_file_content("calculator", "main.py")
test_get_file_content("calculator", "pkg/calculator.py")
test_get_file_content("calculator", "/bin/cat")
test_get_file_content("calculator", "pkg/does_not_exist.py")
