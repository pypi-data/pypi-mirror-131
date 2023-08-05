#pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long, missing-class-docstring
import os
from typing import Dict
from .utils import get_config_value

class DefaultStorageStrategy():
    """
    stores the latest {max_file_count} pictures in the {media_file} textfile
    all other pictures are written to the {complete_media_file} textfile
    """

    def __init__(self, config: Dict, logger) -> None:
        self.log = logger
        self.media_path = get_config_value(config, "media_path")
        self.media_file = get_config_value(config, "media_file")
        self.max_file_count = int(get_config_value(config, "max_file_count"))
        self.complete_media_file = get_config_value(config, "complete_media_file", False)

    def _append_to_complete_media_file(self, filename) -> None:
        if not self.complete_media_file:
            return

        with open(self.complete_media_file, 'a', encoding='utf-8') as binary_file:
            binary_file.write(f'{filename}\n')

    def _add_to_media_file(self, filename) -> None:
        file_data = []
        try:
            with open(self.media_file, 'r', encoding='utf-8') as text_file:
                file_data = text_file.readlines()
        except IOError:
            pass

        file_data.append(f'{filename}\n')
        with open(self.media_file, 'w+', encoding='utf-8') as text_file:
            new_data = file_data[-self.max_file_count:]
            text_file.writelines(new_data)

    def _get_next_filename(self, prefered_filename: str, index: int=0) -> str:
        suffix = f" #{index}" if index > 0 else ''
        new_filename = f'{prefered_filename}{suffix}'
        if os.path.exists(new_filename):
            return self._get_next_filename(prefered_filename, index+1)
        return new_filename

    def store(self, data: bytes, filename: str) -> None:
        target = self._get_next_filename(os.path.join(self.media_path, filename))

        self.log.trace(f'save file as {target}')
        with open(target, "wb") as binary_file:
            binary_file.write(data)
            self._add_to_media_file(target)
            self._append_to_complete_media_file(target)
#pylint: enable=missing-module-docstring, missing-function-docstring, line-too-long, missing-class-docstring
