import os
import shutil


def clean_directory(dir_path: str) -> None:
    if os.path.exists(dir_path):
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


def create_file_path(dir_path: str, file_name: str) -> str:
    return os.path.join(dir_path, file_name)


def rename_file(file_path_from: str, file_path_to: str) -> None:
    if os.path.exists(file_path_from):
        os.rename(file_path_from, file_path_to)


