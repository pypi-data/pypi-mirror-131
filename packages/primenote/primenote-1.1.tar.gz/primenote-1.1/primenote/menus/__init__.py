#!/usr/bin/python3
from pathlib import Path
from PyQt5 import QtCore, QtWidgets

try:
    from ..backend.constants import ConfigDirs
except (ValueError, ImportError):
    from backend.constants import ConfigDirs


class MoveDialog(QtWidgets.QFileDialog):
    """ Self-contained class for the folder move dialog (all modes) """
    def __init__(self, name: str):
        super().__init__()
        self.setDirectory(str(ConfigDirs.NOTES))
        self.setWindowTitle(f"Select a folder for '{name}'")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFileMode(QtWidgets.QFileDialog.Directory)
        self.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog | QtWidgets.QFileDialog.ShowDirsOnly)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.setViewMode(QtWidgets.QFileDialog.Detail)
        self.setModal(True)
        self.directoryEntered.connect(self._entered)
        self.Customize(self)

    def _backOrForwardClicked(self):
        """ Fix for missing Qt signals for back and forward buttons """
        path = self.directory().absolutePath()
        self.directoryEntered.emit(path)

    def _entered(self, current: str):
        """ Prevents navigation outside of notes root directory """
        if ConfigDirs.NOTES not in Path(current).parents:
            self.setDirectory(str(ConfigDirs.NOTES))

    class Customize:
        def __init__(self, dialog):
            self._disableComboBox(dialog)
            for child in (self._fixSignals, self._hideSidePanel, self._treeView):
                try:
                    child(dialog)
                except AttributeError:
                    pass

        def _disableComboBox(self, dialog):
            """ Disables navigation and filetype combo boxes """
            for comboBox in dialog.findChildren(QtWidgets.QComboBox):
                comboBox.setEnabled(False)

        def _fixSignals(self, dialog):
            """ Fix for missing Qt signals for back and forward buttons """
            back = dialog.findChild(QtWidgets.QToolButton, "backButton")
            forward = dialog.findChild(QtWidgets.QToolButton, "forwardButton")
            back.clicked.connect(dialog._backOrForwardClicked)
            forward.clicked.connect(dialog._backOrForwardClicked)

        def _hideSidePanel(self, dialog):
            """ Hides the left shortcut panel """
            listView = dialog.findChild(QtWidgets.QListView)
            listView.hide()

        def _treeView(self, dialog):
            """ Customizes tree view """
            treeView = dialog.findChild(QtWidgets.QTreeView)
            treeView.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # Name
            treeView.header().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)  # Date
            treeView.hideColumn(1)  # Size
            treeView.hideColumn(2)  # Type
