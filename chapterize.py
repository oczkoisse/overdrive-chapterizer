from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QFileSystemModel
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, Qt, QDir, QItemSelection

from Ui_chapterize import Ui_ChapterizeWindow
from mp3file import Mp3File


class ChaptersTableModel(QAbstractTableModel):

    headers = ["Title", "Start", "End"]

    def __init__(self, mp3_filepath=''):
        super().__init__()
        self.set_file(mp3_filepath)

    def set_file(self, mp3_filepath):
        mp3 = None
        if mp3_filepath != '':
            try:
                mp3 = Mp3File(mp3_filepath)
            except IOError:
                return

        self.beginResetModel()
        self._mp3 = mp3
        self.endResetModel()

    def data(self, index, role):
        if self._mp3 is None:
            return None
        if role != Qt.DisplayRole:
            return None
        if not index.isValid():
            return None

        col = index.column()
        row = index.row()

        ch = self._mp3.chapters[row]

        if col == 0:
            return ch.title
        elif col == 1:
            return str(ch.start)
        elif col == 2:
            return str(ch.end)

        return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        return ChaptersTableModel.headers[section]

    def rowCount(self, parent):
        if parent.isValid() or self._mp3 is None:
            return 0
        return len(self._mp3.chapters)

    def columnCount(self, parent):
        if parent.isValid():
            return 0
        return len(ChaptersTableModel.headers)


class Chapterize(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ChapterizeWindow()
        self.ui.setupUi(self)

        self.ui.actionChangeDir.triggered.connect(self.onActionChangeDirectory)
        self.ui.actionExit.triggered.connect(self.close)

        self.dir = QDir.homePath()

        self.chaptersTableModel = ChaptersTableModel()
        self.ui.chapterTable.setModel(self.chaptersTableModel)

        self.mp3ListModel = QFileSystemModel()
        self.mp3ListModel.setNameFilters(['*.mp3'])
        self.mp3ListModel.setFilter(QDir.Files)
        self.mp3ListModel.setRootPath(self.dir)
        self.mp3ListModel.setNameFilterDisables(False)

        self.ui.mp3List.setModel(self.mp3ListModel)
        self.ui.mp3List.setRootIndex(self.mp3ListModel.index(self.dir))
        self.ui.mp3List.selectionModel().selectionChanged.connect(self.onSelectionChanged)

    @pyqtSlot()
    def onActionChangeDirectory(self):
        chosen_dir = QFileDialog.getExistingDirectory(self, "Change Directory...", self.dir, QFileDialog.ShowDirsOnly)
        if chosen_dir != '':
            self.dir = chosen_dir
            self.mp3ListModel.setRootPath(self.dir)
            self.ui.mp3List.setRootIndex(self.mp3ListModel.index(self.dir))

    @pyqtSlot(QItemSelection, QItemSelection)
    def onSelectionChanged(self, selected, deselected):
        sel_idx = selected.indexes()[0]
        pth = self.mp3ListModel.fileInfo(sel_idx).absoluteFilePath()
        self.chaptersTableModel.set_file(pth)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wdw = Chapterize()
    wdw.show()
    sys.exit(app.exec_())
