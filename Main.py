#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################
import sys
from myTreeViewCode import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.view = myTreeView(self.centralwidget)
        self.view.setObjectName("view")
        self.vboxlayout.addWidget(self.view)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 31))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.actionsMenu = QtWidgets.QMenu(self.menubar)
        self.actionsMenu.setObjectName("actionsMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        '''
        self.exitAction = QtWidgets.QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.insertRowAction = QtWidgets.QAction(MainWindow)
        self.insertRowAction.setObjectName("insertRowAction")
        self.removeRowAction = QtWidgets.QAction(MainWindow)
        self.removeRowAction.setObjectName("removeRowAction")
        self.insertColumnAction = QtWidgets.QAction(MainWindow)
        self.insertColumnAction.setObjectName("insertColumnAction")
        self.removeColumnAction = QtWidgets.QAction(MainWindow)
        self.removeColumnAction.setObjectName("removeColumnAction")
        self.insertChildAction = QtWidgets.QAction(MainWindow)
        self.insertChildAction.setObjectName("insertChildAction")
        self.fileMenu.addAction(self.exitAction)
        self.actionsMenu.addAction(self.insertRowAction)
        self.actionsMenu.addAction(self.insertColumnAction)
        self.actionsMenu.addSeparator()
        self.actionsMenu.addAction(self.removeRowAction)
        self.actionsMenu.addAction(self.removeColumnAction)
        self.actionsMenu.addSeparator()
        self.actionsMenu.addAction(self.insertChildAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.actionsMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        '''
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Editable Tree Model"))
        self.fileMenu.setTitle(_translate("MainWindow", "&File"))
        self.actionsMenu.setTitle(_translate("MainWindow", "&Actions"))
        self.exitAction.setText(_translate("MainWindow", "E&xit"))
        self.exitAction.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.insertRowAction.setText(_translate("MainWindow", "Insert Row"))
        self.insertRowAction.setShortcut(_translate("MainWindow", "Ctrl+I, R"))
        self.removeRowAction.setText(_translate("MainWindow", "Remove Row"))
        self.removeRowAction.setShortcut(_translate("MainWindow", "Ctrl+R, R"))
        self.insertColumnAction.setText(_translate("MainWindow", "Insert Column"))
        self.insertColumnAction.setShortcut(_translate("MainWindow", "Ctrl+I, C"))
        self.removeColumnAction.setText(_translate("MainWindow", "Remove Column"))
        self.removeColumnAction.setShortcut(_translate("MainWindow", "Ctrl+R, C"))
        self.insertChildAction.setText(_translate("MainWindow", "Insert Child"))
        self.insertChildAction.setShortcut(_translate("MainWindow", "Ctrl+N"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        headers = ("Tag", "Database Row", "Sort Column", "DB Parent Row YY")
        # self.exitAction.triggered.connect(QApplication.instance().quit)
        # self.view.selectionModel().selectionChanged.connect(self.updateActions)
        # self.actionsMenu.aboutToShow.connect(self.updateActions)
        # self.insertRowAction.triggered.connect(self.insertRow)
        # self.insertColumnAction.triggered.connect(self.insertColumn)
        # self.removeRowAction.triggered.connect(self.removeRow)
        # self.removeColumnAction.triggered.connect(self.removeColumn)
        # self.insertChildAction.triggered.connect(self.insertChild)

        # self.updateActions()
    '''
    def insertChild(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if model.columnCount(index) == 0:
            if not model.insertColumn(0, index):
                return

        if not model.insertRow(0, index):
            return

        for column in range(model.columnCount(index)):
            child = model.index(0, column, index)
            model.setData(child, "[No data]", Qt.EditRole)
            if model.headerData(column, Qt.Horizontal) is None:
                model.setHeaderData(column, Qt.Horizontal, "[No header]",
                        Qt.EditRole)

        self.view.selectionModel().setCurrentIndex(model.index(0, 0, index),
                QItemSelectionModel.ClearAndSelect)
        self.updateActions()

    def insertColumn(self):
        model = self.view.model()
        column = self.view.selectionModel().currentIndex().column()

        changed = model.insertColumn(column + 1)
        if changed:
            model.setHeaderData(column + 1, Qt.Horizontal, "[No header]",
                    Qt.EditRole)

        self.updateActions()

        return changed

    def insertRow(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if not model.insertRow(index.row()+1, index.parent()):
            return

        self.updateActions()

        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row()+1, column, index.parent())
            model.setData(child, "[No data]", Qt.EditRole)

    def removeColumn(self):
        model = self.view.model()
        column = self.view.selectionModel().currentIndex().column()

        changed = model.removeColumn(column)
        if changed:
            self.updateActions()

        return changed

    def removeRow(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if (model.removeRow(index.row(), index.parent())):
            self.updateActions()

    def updateActions(self):
        hasSelection = not self.view.selectionModel().selection().isEmpty()
        self.removeRowAction.setEnabled(hasSelection)
        self.removeColumnAction.setEnabled(hasSelection)

        hasCurrent = self.view.selectionModel().currentIndex().isValid()
        self.insertRowAction.setEnabled(hasCurrent)
        self.insertColumnAction.setEnabled(hasCurrent)

        if hasCurrent:
            self.view.closePersistentEditor(self.view.selectionModel().currentIndex())

            row = self.view.selectionModel().currentIndex().row()
            column = self.view.selectionModel().currentIndex().column()
            if self.view.selectionModel().currentIndex().parent().isValid():
                self.statusBar().showMessage("Position: (%d,%d)" % (row, column))
            else:
                self.statusBar().showMessage("Position: (%d,%d) in top level" % (row, column))
    '''

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())