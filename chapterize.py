from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, Qt

from Ui_chapterize import Ui_ChapterizeWindow
from mp3file import Mp3File


class ChaptersTableModel(QAbstractTableModel):

    headers = ["Title", "Start", "End", "Filename"]

    def __init__(self, dir):
        super().__init__()
        self._all_chapters = []

        for mp3_filepath in Path(dir).glob('*.mp3'):
            mp3 = Mp3File(mp3_filepath)
            self._all_chapters.extend(list(zip(mp3.chapters, [mp3] * len(mp3.chapters))))

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return None
        if not index.isValid():
            return None

        col = index.column()
        row = index.row()

        ch, mp3 = self._all_chapters[row]

        if col == 0:
            return ch.title
        elif col == 1:
            return str(ch.start)
        elif col == 2:
            return str(ch.end)
        elif col == 3:
            return mp3.path.name

        return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        return ChaptersTableModel.headers[section]

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self._all_chapters)

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
        self.dir = ""

    @pyqtSlot()
    def onActionChangeDirectory(self):
        self.dir = QFileDialog.getExistingDirectory(self, "Change Directory...", self.dir)
        self.model = ChaptersTableModel(self.dir)
        self.ui.chapterTable.setModel(self.model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wdw = Chapterize()
    wdw.show()
    sys.exit(app.exec_())
