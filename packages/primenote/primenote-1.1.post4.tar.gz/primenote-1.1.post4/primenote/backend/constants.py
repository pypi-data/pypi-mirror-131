#!/usr/bin/python3
import os
import sys
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from PyQt5.QtGui import QTextFragment
try:
    from ..__id__ import ID
    from ..backend import DeepPath
except (ValueError, ImportError):
    from __id__ import ID
    from backend import DeepPath

DESKTOP_ENVIRONMENT = os.environ.get("DESKTOP_SESSION")
STYLE_DEFAULT = "minimal.css"
PALETTE_DEFAULT = "northern.css"


def configDir() -> Path:
    if sys.platform.startswith("win"):
        return Path.home() / ID
    return Path.home() / ".config" / ID


@dataclass
class ConfigDirs:
    CFG = configDir()
    NOTES = DeepPath(configDir() / "notes")
    ARCHIVES = CFG / "archives"
    LOGS = CFG / "logs"
    PALETTES = CFG / "ui" / "palettes"
    STYLES = CFG / "ui" / "styles"
    TERMINAL = CFG / "ui" / "terminal"
    TRASH = CFG / "trash"
    VIM = CFG / "ui" / "vim"


@dataclass
class ConfigFiles:
    CSS = ConfigDirs.CFG / "ui" / "global.css"
    LOG = ConfigDirs.LOGS / "session.log"
    NOTES = ConfigDirs.CFG / "notes.json"
    PROFILES = ConfigDirs.CFG / "profiles.json"
    SETTINGS = ConfigDirs.CFG / "settings.json"
    VIM = ConfigDirs.VIM / "vimrc"


@dataclass
class RootDirs:
    ROOT = Path(__file__).parents[1]
    FONTS = ROOT / "ui" / "fonts"
    ICONS = ROOT / "ui" / "icons"
    PALETTES = ROOT / "ui" / "palettes"
    STYLES = ROOT / "ui" / "styles"
    TERMINAL = ROOT / "ui" / "terminal"
    VIM = ROOT / "ui" / "vim"
    WIZARD = ROOT / "ui" / "wizard"


@dataclass
class RootFiles:
    CSS = RootDirs.ROOT / "ui" / "global.css"
    VIM = RootDirs.ROOT / "vim" / "vimrc"
    DEFAULT_STYLE = RootDirs.STYLES / STYLE_DEFAULT
    DEFAULT_PALETTE = RootDirs.PALETTES / PALETTE_DEFAULT


@dataclass
class CoreActions:
    tray: dict
    browser: dict


@dataclass
class Cursor:
    pos: int
    anchor: int
    fragment: QTextFragment = None


@dataclass
class Tuples:
    Action = namedtuple("Action", ("label", "icon", "call"))
    Cleaner = namedtuple("Cleaner", ("dir", "delay"))
    Mime = namedtuple("Mime", ("type", "data"))
    Mode = namedtuple("Mode", ("icon", "label"))
    NoteIcons = namedtuple("NoteIcons", ("menu", "toolbar"))
    RegexCSS = namedtuple("RegexCSS", ("selector", "elements", "property"))
    SizeGrips = namedtuple("SizeGrips", ("left", "center", "right"))
    Stylesheet = namedtuple("Stylesheet", ("profile", "fallback"))
