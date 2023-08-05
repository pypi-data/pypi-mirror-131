import os


def get_filenames_in_folder(path: str) -> list:
    """Given a folder path, get a list of filenames in that folder."""
    file_list = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if filename not in file_list:
                file_list.append(filename)
    file_list.sort()
    return file_list


def get_subfolder_names_in_folder(path: str) -> list:
    """Get a list of subfolder names inside a folder."""
    folder_list = []
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            folder_list.append(name)
    folder_list.sort()
    return folder_list
