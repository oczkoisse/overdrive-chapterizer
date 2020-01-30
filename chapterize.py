from pathlib import Path
import sys

from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QFileSystemModel, QMenu, QAction
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, Qt, QDir, QItemSelection, QModelIndex

from Ui_chapterize import Ui_ChapterizeWindow
from mp3file import Mp3File
from chapter import Chapter
from timestamp import Timestamp

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

    def data(self, index, role=Qt.DisplayRole):
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

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        return ChaptersTableModel.headers[section]

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid() or self._mp3 is None:
            return 0
        return len(self._mp3.chapters)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(ChaptersTableModel.headers)

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row+count-1)
        for i in range(count):
            self._mp3.chapters.insert(row + i, Chapter(title='', start=Timestamp(), end=Timestamp()))
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row+count-1)
        for _ in range(count):
            self._mp3.chapters.pop(row)
        self.endRemoveRows()
        return True


class Chapterize(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ChapterizeWindow()
        self.ui.setupUi(self)

        self.ui.actionChangeDir.triggered.connect(self.onDirectoryChange)
        self.ui.actionExit.triggered.connect(self.close)

        self.dir = QDir.homePath()

        self.chaptersTableModel = ChaptersTableModel()
        self.ui.chapterTable.setModel(self.chaptersTableModel)

        self.ui.chapterTable.contextMenuEvent = self.onChapterContextMenu

        self.mp3ListModel = QFileSystemModel()
        self.mp3ListModel.setNameFilters(['*.mp3'])
        self.mp3ListModel.setFilter(QDir.Files)
        self.mp3ListModel.setRootPath(self.dir)
        self.mp3ListModel.setNameFilterDisables(False)

        self.ui.mp3List.setModel(self.mp3ListModel)
        self.ui.mp3List.setRootIndex(self.mp3ListModel.index(self.dir))
        self.ui.mp3List.selectionModel().selectionChanged.connect(self.onMp3Select)

    @pyqtSlot()
    def onDirectoryChange(self):
        chosen_dir = QFileDialog.getExistingDirectory(self, "Change Directory...", self.dir, QFileDialog.ShowDirsOnly)
        if chosen_dir != '':
            self.dir = chosen_dir
            self.mp3ListModel.setRootPath(self.dir)
            self.ui.mp3List.setRootIndex(self.mp3ListModel.index(self.dir))

    @pyqtSlot(QItemSelection, QItemSelection)
    def onMp3Select(self, selected, deselected):
        sel_idx = selected.indexes()[0]
        pth = self.mp3ListModel.fileInfo(sel_idx).absoluteFilePath()
        self.chaptersTableModel.set_file(pth)

    @pyqtSlot(QContextMenuEvent)
    def onChapterContextMenu(self, e: QContextMenuEvent):
        idx = self.ui.chapterTable.indexAt(e.pos())
        row = idx.row()
        if row < 0:
            row = self.chaptersTableModel.rowCount()

        menu = QMenu(self)

        insertAction = QAction('&Insert', menu)
        insertAction.triggered.connect(lambda: self.chaptersTableModel.insertRow(row))

        menu.addAction(insertAction)

        deleteAction = QAction('&Delete', menu)
        deleteAction.triggered.connect(lambda: self.chaptersTableModel.removeRow(row))

        menu.addAction(deleteAction)

        menu.exec_(e.globalPos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wdw = Chapterize()
    wdw.show()
    sys.exit(app.exec_())
