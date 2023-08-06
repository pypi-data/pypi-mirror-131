#!/usr/bin/python3
from pathlib import Path
from typing import Tuple
from PyQt5 import QtCore, QtWidgets

try:
    from ..backend import logger
    from ..backend.constants import ConfigDirs, Tuples, DESKTOP_ENVIRONMENT
except (ValueError, ImportError):
    from backend import logger
    from backend.constants import ConfigDirs, Tuples, DESKTOP_ENVIRONMENT

log = logger.new(__name__)


def sortQActions(data: list) -> list:
    """ Sorts a list of QMenus or QActions """
    try:
        return sorted(data, key=lambda item: item.title().lower())
    except AttributeError:
        return sorted(data, key=lambda item: item.text().lower())


class AbstractNoteAction(QtWidgets.QAction):
    def __init__(self, parent: QtWidgets.QMenu, path: Path):
        super().__init__(parent)
        self.core = parent.core
        self.path = path
        self.setCheckable(True)
        self.triggered.connect(self._triggered)
        self._setIcon()
        self._setText()

    def _setIcon(self):
        """ Sets an icon according to note type """
        nid = str(self.path.relative_to(ConfigDirs.NOTES))
        try:
            mode = self.core.pdb[nid]["mode"]
            prefix = mode if mode in ("html", "image") else "plain"
        except KeyError:
            prefix = "image" if self.path.suffix == ".png" else "plain"

        favorites = self.core.ndb["favorites"]
        suffix = "starred" if nid in favorites else "regular"
        icon = self.core.icons[f"{prefix}_{suffix}"]
        self.setIcon(icon)

    def _setText(self) -> str:
        """ Sets filename as QAction text, truncates string if longer than threshold value """
        threshold = self.core.sdb["general"]["truncate threshold"]
        label = self.path.stem
        if len(label) > threshold:
            label = f"{label[:threshold]} ..."
        self.setText(label)


class CoreAction(QtWidgets.QAction):
    def __init__(self, core, action: Tuples.Action, path: Path = None):
        super().__init__(core)
        self.path = path
        self.action = action
        self.setIcon(action.icon)
        self.setText(action.label)
        self.triggered.connect(self._triggered)

    def _triggered(self):
        """ Handles left click event, calls an action """
        if self.path:
            log.info(f"Core : {self.action.label} : {self.path}")
            self.action.call(self.path)
        else:
            log.info(f"Core : {self.action.label}")
            self.action.call()


class CoreMenu(QtWidgets.QMenu):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.icons = core.icons
        self.aboutToShow.connect(self._refresh)

        # Preload menu to prevent odd appearance and others problems
        if DESKTOP_ENVIRONMENT in ("cinnamon", "xfce"):
            self.popup(QtCore.QPoint(0, 0))
            self.hide()

    def addFoldersList(self):
        """ Adds root level folders top menus """
        folders = [f for f in ConfigDirs.NOTES.iterdir() if f.is_dir()]
        folders = [SubMenu(self, f) for f in folders]
        for f in sortQActions(folders):
            self.addMenu(f)

    def addNotesList(self):
        """ Inserts QActions for locals (root) and loaded sub-notes """
        def hasParents(path: Path) -> bool:
            """ Verifies if a note is located at the root of the notes directory """
            parents = path.relative_to(ConfigDirs.NOTES)
            return bool(parents.parts[:-1])

        def isNote(path: Path) -> bool:
            return path.is_file() and path.suffix in (".txt", ".png")

        def noneAction(self) -> QtWidgets.QWidgetAction:
            """ Adds a message when the note repository is empty """
            label = QtWidgets.QLabel("Note folder is empty")
            label.setAlignment(QtCore.Qt.AlignCenter)
            font = label.font()
            font.setItalic(True)
            label.setFont(font)
            action = QtWidgets.QWidgetAction(self)
            action.setDefaultWidget(label)
            return action

        notes = [self.RootNoteAction(self, f) for f in ConfigDirs.NOTES.iterdir() if isNote(f)]
        for item in sortQActions(notes):
            self.addAction(item)

        subnotes = [self.RootNoteAction(self, f, prefix=True) for f in self.core.loaded if hasParents(f)]
        for item in sortQActions(subnotes):
            self.addAction(item)

        if not notes and not subnotes:
            item = noneAction(self)
            self.addAction(item)

    def _refresh(self):
        """ Updates core menu on request """
        self.clear()
        for key in self.core.sdb["core menus"]["tray"]:
            if key == "separator":
                self.addSeparator()
            elif key == "folders list":
                self.addFoldersList()
            elif key == "notes list":
                self.addNotesList()
            else:
                action = self.core.actions.tray[key]
                action = CoreAction(self.core, action)
                self.addAction(action)

    class RootNoteAction(AbstractNoteAction):
        def __init__(self, parent: QtWidgets.QMenu, path: Path, prefix=False):
            super().__init__(parent, path)
            if self.path in self.core.loaded:
                isVisible = self.core.loaded[path].isVisible()
                self.setChecked(isVisible)

            if prefix:
                db = ConfigDirs.NOTES
                parents = self.path.relative_to(db).parts[:-1]
                parents = " / ".join(parents)
                self.setText(f"{parents} / {self.text()}")

        def _triggered(self):
            """ Handles left click event, toggles a note """
            self.core.notes.toggle(self.path)


class SubMenu(QtWidgets.QMenu):
    def __init__(self, parent: QtWidgets.QMenu, path: Path):
        super().__init__(parent)
        self.core = parent.core
        self.path = path
        self.setTitle(path.name)
        self.aboutToShow.connect(self._refresh)

        loaded = self._loadedCount(path)
        title = f"{path.name} ({loaded})" if loaded else f"{path.name}"
        icon = "folder_active" if loaded else "folder_inactive"
        icon = self.core.icons[icon]
        self.setTitle(title)
        self.setIcon(icon)

    def _addSubActions(self, actions: Tuple):
        """ Adds core actions """
        for key in actions:
            if key == "separator":
                self.addSeparator()
            else:
                action = self.core.actions.browser[key]
                action = CoreAction(self.core, action, self.path)
                self.addAction(action)

    def _loadedCount(self, path: Path) -> int:
        """ Counts how many notes of a folder are currently loaded """
        count = 0
        for f in self.core.loaded:
            if f.is_relative_to(self.path):
                count += 1
        return count

    def _refresh(self):
        """ Updates sub-menus on request """
        def isNote(self) -> bool:
            """ Verifies if the path point to a note file """
            return self.is_file() and self.suffix in (".png", ".txt")

        self.clear()
        folders = [f for f in self.path.iterdir() if f.is_dir()]
        folders = [SubMenu(self, f) for f in folders]
        for menu in sortQActions(folders):
            self.addMenu(menu)

        files = [f for f in self.path.iterdir() if isNote(f)]
        files = [self.SubNoteAction(self, f) for f in files]
        for note in sortQActions(files):
            self.addAction(note)

        if files or folders:
            actions = self.core.sdb["core menus"]["browser"]
        else:
            actions = ("new", "rename", "move", "open", "separator", "delete")
        self._addSubActions(actions)

    class SubNoteAction(AbstractNoteAction):
        def __init__(self, parent: QtWidgets.QMenu, path: Path):
            super().__init__(parent, path)
            self.setChecked(self.path in self.core.loaded)

        def _triggered(self):
            """ Handles left click event, toggles a sub-note """
            if self.path in self.core.loaded:
                self.core.notes.close(self.path)
            else:
                self.core.notes.add(self.path)
