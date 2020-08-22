import os
import re
from typing import List

audio_extensions = {'.mp3', '.flac', '.aac', '.mp4', '.m4a', '.m4b', '.m4p', '.mmf', '.mpc' '.wav', '.ape', '.wv',
                    '.aiff', '.au', '.pcm', '.wma', '.aa', '.aax', '.alac', '.amr', '.au', '.awb', '.dct', '.dss',
                    '.dvf', '.gsm', '.iklax', '.ivs', '.ogg', '.oga', '.mogg', '.ra', '.sln', '.tta', '.8svx'}


def get_release_dirs(folder: str) -> List[str]:
    files = []
    subdirs = []

    for curr in os.scandir(folder):
        if curr.is_file():
            files.append(curr.path)
        elif curr.is_dir():
            subdirs.append(curr.path)

    # no subfolders, media files present
    if (not subdirs and has_media_files(files)) or (subdirs and subdirs_are_discs(subdirs)):
        yield folder

    else:
        for subdir in subdirs:
            yield from get_release_dirs(subdir)


def has_media_files(files: List[str]) -> bool:
    result = False

    for file in files:
        if has_audio_extension(file):
            result = True

    return result


def has_audio_extension(path):
    return os.path.splitext(path)[1].lower() in audio_extensions


def subdirs_are_discs(subdirs: List[str]) -> bool:
    # sanity check
    if len(subdirs) > 20:
        return False

    curr_disc = []
    curr_not_disc = []

    for curr in subdirs:
        folder_name = curr.split(os.path.sep)[-1]
        if re.findall(r'(disc|disk|cd|part) ?\d{1,2}', folder_name.lower()) or "bonus" in folder_name.lower():
            files = [file.path for file in os.scandir(curr) if os.path.isfile(file)]
            if has_media_files(files):
                curr_disc.append(curr)
            else:
                curr_not_disc.append(curr)
        else:
            curr_not_disc.append(curr)

        # there cannot be more than 10 non-disc entries in the directory
        if len(curr_not_disc) > 5:
            return False

    # at least 2 subdirs need to be discs
    if len(curr_disc) < 2:
        return False

    # if any of the subfolders are more than 5MB (excluding images), return False
    for curr in curr_not_disc:
        if get_dir_size(curr) > 5 * 1024 * 1024:
            return False

    return True


def get_dir_size(dir: str) -> int:
    size = 0

    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in ['.png', '.jpg', '.jpeg', '.jpe', '.bmp']:
                size += os.path.getsize(os.path.join(dirpath, filename))

    return size

    #return sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(dir)
    #           for filename in filenames)
