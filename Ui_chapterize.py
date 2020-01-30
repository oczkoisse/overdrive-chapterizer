# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Chapterize.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChapterizeWindow(object):
    def setupUi(self, ChapterizeWindow):
        ChapterizeWindow.setObjectName("ChapterizeWindow")
        ChapterizeWindow.resize(821, 601)
        self.centralwidget = QtWidgets.QWidget(ChapterizeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mp3List = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mp3List.sizePolicy().hasHeightForWidth())
        self.mp3List.setSizePolicy(sizePolicy)
        self.mp3List.setObjectName("mp3List")
        self.horizontalLayout.addWidget(self.mp3List)
        self.chapterTable = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chapterTable.sizePolicy().hasHeightForWidth())
        self.chapterTable.setSizePolicy(sizePolicy)
        self.chapterTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.chapterTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.chapterTable.setObjectName("chapterTable")
        self.chapterTable.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.chapterTable)
        ChapterizeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ChapterizeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        ChapterizeWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(ChapterizeWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionChangeDir = QtWidgets.QAction(ChapterizeWindow)
        self.actionChangeDir.setObjectName("actionChangeDir")
        self.actionSave = QtWidgets.QAction(ChapterizeWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(ChapterizeWindow)
        self.actionExit.setObjectName("actionExit")
        self.menu_File.addAction(self.actionChangeDir)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionSave)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionExit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(ChapterizeWindow)
        QtCore.QMetaObject.connectSlotsByName(ChapterizeWindow)

    def retranslateUi(self, ChapterizeWindow):
        _translate = QtCore.QCoreApplication.translate
        ChapterizeWindow.setWindowTitle(_translate("ChapterizeWindow", "Chapterize"))
        self.menu_File.setTitle(_translate("ChapterizeWindow", "&File"))
        self.actionOpen.setText(_translate("ChapterizeWindow", "&Open"))
        self.actionChangeDir.setText(_translate("ChapterizeWindow", "Change &Directory..."))
        self.actionSave.setText(_translate("ChapterizeWindow", "&Save"))
        self.actionExit.setText(_translate("ChapterizeWindow", "&Exit"))
