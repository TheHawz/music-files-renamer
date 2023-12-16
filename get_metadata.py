from pathlib import Path
from typing import List

from mutagen import File, mp3


def _parse_artist_list(input: List[str], sep=' x '):
    if not isinstance(input, List):
        return input

    joined_str = sep.join(input)
    joined_str = joined_str.replace(', ', ' x ')
    return joined_str


def _parse_title_list(input: List[str]):
    if not isinstance(input, List):
        return input
    if len(input) > 1:
        print('[WARNING] Title is a list with more than one entry...')
        return ' '.join(input)
    return input[0]


def is_music(file_path: str | Path) -> float:
    try:
        file = mp3.MP3(file_path)
        _ = file.info.length
    except mp3.HeaderNotFoundError:
        return False

    return True


def get_metadata_from_file(file_path: str | Path) -> dict:
    file = File(file_path)

    artist = _parse_artist_list(file['TPE1'].text)

    title = _parse_title_list(file['TIT2'].text)

    return {
        'artist': artist,
        'title': title,
    }
