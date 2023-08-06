#!/usr/bin/python3
from glob import glob
from pathlib import Path


def sanitizeFileName(text: str, default: str = ""):
    """ Ensures that the filename are compliant with Windows and POSIX standards """
    illegal = ("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7",
               "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9")
    if text.upper() in illegal:
        return default

    for c in '\\/:*?"<>|':
        text = text.replace(c, "")
    text = text.replace("..", "")
    return text


class DeepPath(Path):
    _flavour = type(Path())._flavour

    def is_empty(self) -> bool:
        """ Verifies if a file or a directory is empty """
        if self.is_dir():
            empty = not [f for f in self.rglob("*")]
            return empty and not self.is_symlink()

        elif self.is_file():
            empty = self.stat().st_size == 0
            return empty

    def is_relative_to(self, *other):  # Legacy support for Python 3.8.7 (added in Python 3.9)
        """ Returns True if the path is relative to another path or False """
        try:
            self.relative_to(*other)
            return True
        except ValueError:
            return False

    def rglob(self, pattern: str) -> list:
        """ Search directory recursively """
        # glob.glob temporarily replaces pathlib.glob to support directory links
        # see https://bugs.python.org/issue33428 (2018)
        path = str(self / "**" / pattern)
        found = glob(path, recursive=True)
        return [DeepPath(f) for f in found]
