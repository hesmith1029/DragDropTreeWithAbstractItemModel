#!/usr/bin/env python

############################################################################
#
# Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
#
# This file is part of the example classes of the Qt Toolkit.
#
# This file may be used under the terms of the GNU General Public
# License version 2.0 as published by the Free Software Foundation
# and appearing in the file LICENSE.GPL included in the packaging of
# this file.  Please review the following information to ensure GNU
# General Public Licensing requirements will be met:
# http://www.trolltech.com/products/qt/opensource.html
#
# If you are unsure which license is appropriate for your use, please
# review the following information:
# http://www.trolltech.com/products/qt/licensing.html or contact the
# sales department at sales@trolltech.com.
#
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##############################################################################
import sys
from myTreeViewCode import *


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(400, 800)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.view = myTreeView(self.centralwidget)
        self.view.setObjectName("view")
        self.vboxlayout.addWidget(self.view)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 31))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.actionsMenu = QtWidgets.QMenu(self.menubar)
        self.actionsMenu.setObjectName("actionsMenu")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.exitAction = QtWidgets.QAction(main_window)
        self.exitAction.setObjectName("exitAction")
        self.insertRowAction = QtWidgets.QAction(main_window)
        self.insertRowAction.setObjectName("insertRowAction")
        self.removeRowAction = QtWidgets.QAction(main_window)
        self.removeRowAction.setObjectName("removeRowAction")
        self.insertColumnAction = QtWidgets.QAction(main_window)
        self.insertColumnAction.setObjectName("insertColumnAction")
        self.removeColumnAction = QtWidgets.QAction(main_window)
        self.removeColumnAction.setObjectName("removeColumnAction")
        self.insertChildAction = QtWidgets.QAction(main_window)
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

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Editable Tree Model"))
        self.fileMenu.setTitle(_translate("main_window", "&File"))
        self.actionsMenu.setTitle(_translate("main_window", "&Actions"))
        self.exitAction.setText(_translate("main_window", "E&xit"))
        self.exitAction.setShortcut(_translate("main_window", "Ctrl+Q"))
        self.insertRowAction.setText(_translate("main_window", "Insert Row"))
        self.insertRowAction.setShortcut(_translate("main_window", "Ctrl+I, R"))
        self.removeRowAction.setText(_translate("main_window", "Remove Row"))
        self.removeRowAction.setShortcut(_translate("main_window", "Ctrl+R, R"))
        self.insertColumnAction.setText(_translate("main_window", "Insert Column"))
        self.insertColumnAction.setShortcut(_translate("main_window", "Ctrl+I, C"))
        self.removeColumnAction.setText(_translate("main_window", "Remove Column"))
        self.removeColumnAction.setShortcut(_translate("main_window", "Ctrl+R, C"))
        self.insertChildAction.setText(_translate("main_window", "Insert Child"))
        self.insertChildAction.setShortcut(_translate("main_window", "Ctrl+N"))


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup_ui(self)
        self.exitAction.triggered.connect(QApplication.instance().quit)
        # self.view.selectionModel().selectionChanged.connect(self.updateActions)
        # self.actionsMenu.aboutToShow.connect(self.updateActions)
        # self.insertRowAction.triggered.connect(self.insertRow)
        # self.insertColumnAction.triggered.connect(self.insertColumn)
        # self.removeRowAction.triggered.connect(self.removeRow)
        # self.removeColumnAction.triggered.connect(self.removeColumn)
        # self.insertChildAction.triggered.connect(self.insertChild)

        # self.updateActions()

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



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())