from pathlib import Path


def prepare_file_system(valid_file_content=None, non_existent_file=False,
                        directory_instead_of_file=False, unreadable_file=False):
    """
    Step to set up file system states for testing.
    """
    def step(context):
        base_dir = Path("/tmp/test_process_file")
        base_dir.mkdir(parents=True, exist_ok=True)

        if valid_file_content:
            file_path = base_dir / "valid_file.txt"
            file_path.write_text(valid_file_content)
            context.file_path = str(file_path)
        elif non_existent_file:
            context.file_path = str(base_dir / "non_existent_file.txt")
        elif directory_instead_of_file:
            directory_path = base_dir / "test_dir"
            directory_path.mkdir(parents=True, exist_ok=True)
            context.file_path = str(directory_path)
        elif unreadable_file:
            file_path = base_dir / "unreadable_file.txt"
            file_path.write_text("Content")
            file_path.chmod(0o000)
            context.file_path = str(file_path)

    return step


def create_invalid_file():
    """
    Step to create a deliberately invalid file for testing.
    """
    def step(context):
        base_dir = Path("/tmp/test_process_file")
        base_dir.mkdir(parents=True, exist_ok=True)

        file_path = base_dir / "invalid_file.txt"
        file_path.touch()
        context.file_path = str(file_path)

    return step
