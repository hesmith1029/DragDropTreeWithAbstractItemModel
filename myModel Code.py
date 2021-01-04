from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# this is a change
# this is another change
# this is a third change

SSSdfsafsafafd

class myModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(myModel, self).__init__(parent)
        from PyQt5 import QtCore, QtWidgets
        from PyQt5.QtWidgets import *
        from PyQt5.QtGui import *
        from PyQt5.QtCore import *
        from PyQt5.QtCore import QVariant
        from pickle import *
        import photo_database_code
        from photo_database_code import *

        SortRole = Qt.UserRole + 1

        class PyMimeData(QMimeData):
            """ The PyMimeData wraps a Python instance as MIME data.
            """
            # The MIME type for instances.
            # MIME_TYPE = QString('application/x-ets-qt4-instance')
            MIME_TYPE = 'application/x-ets-qt5-instance'  # maybe qt5

            def __init__(self, data=None):
                """ Initialise the instance.
                """
                # Required
                QMimeData.__init__(self)

                # Keep a local reference to be returned if possible.
                self._local_instance = data

                if data is not None:
                    # We may not be able to pickle the data.
                    try:
                        pdata = dumps(data)
                    except:
                        return

                    # This format (as opposed to using a single sequence) allows the
                    # type to be extracted without unpickling the data itself.
                    self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)
                print("exiting __init__ of pymimedata")

            @classmethod
            def coerce(cls, md):
                """ Coerce a QMimeData instance to a PyMimeData instance if
        possible.
                """
                # See if the data is already of the right type.  If it is then we know
                # we are in the same process.
                print("In classmethod - PyMimeData")
                if isinstance(md, cls):
                    return md

                # See if the data type is supported.
                if not md.hasFormat(cls.MIME_TYPE):
                    return None

                nmd = cls()
                nmd.setData(cls.MIME_TYPE, md.data())

                return nmd

            def instance(self):
                """ Return the instance.
                """
                print("Entered instance of PyMimeData")
                if self._local_instance is not None:
                    return self._local_instance

                io = StringIO(str(self.data(self.MIME_TYPE)))

                try:
                    # Skip the type.
                    load(io)

                    # Recreate the instance.
                    return load(io)
                except:
                    print("load failed - instance - PyMimeData")
                    pass

                return None

            def instanceType(self):
                print("entered instanceType")
                """ Return the type of the instance.
                """
                if self._local_instance is not None:
                    return self._local_instance.__class__

                try:
                    return loads(str(self.data(self.MIME_TYPE)))
                except:
                    print("instanceType, load failed.")
                    pass

                return None

            ''' 
            Note.  TreeItem was built subclassing Qobject.  Then at the last it was converted to subclass QStandardItem.   
            Most likely it could be simplified.
            Some methods may need to renamed to over write QStandardItem methods that accomplish the same thing.
            '''

        from PyQt5 import QtCore, QtWidgets
        from PyQt5.QtWidgets import *
        from PyQt5.QtGui import *
        from PyQt5.QtCore import *
        from PyQt5.QtCore import QVariant
        from pickle import *
        import photo_database_code
        from photo_database_code import *

        SortRole = Qt.UserRole + 1

        class PyMimeData(QMimeData):
            """ The PyMimeData wraps a Python instance as MIME data.
            """
            # The MIME type for instances.
            # MIME_TYPE = QString('application/x-ets-qt4-instance')
            MIME_TYPE = 'application/x-ets-qt5-instance'  # maybe qt5

            def __init__(self, data=None):
                """ Initialise the instance.
                """
                # Required
                QMimeData.__init__(self)

                # Keep a local reference to be returned if possible.
                self._local_instance = data

                if data is not None:
                    # We may not be able to pickle the data.
                    try:
                        pdata = dumps(data)
                    except:
                        return

                    # This format (as opposed to using a single sequence) allows the
                    # type to be extracted without unpickling the data itself.
                    self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)
                print("exiting __init__ of pymimedata")

            @classmethod
            def coerce(cls, md):
                """ Coerce a QMimeData instance to a PyMimeData instance if
        possible.
                """
                # See if the data is already of the right type.  If it is then we know
                # we are in the same process.
                print("In classmethod - PyMimeData")
                if isinstance(md, cls):
                    return md

                # See if the data type is supported.
                if not md.hasFormat(cls.MIME_TYPE):
                    return None

                nmd = cls()
                nmd.setData(cls.MIME_TYPE, md.data())

                return nmd

            def instance(self):
                """ Return the instance.
                """
                print("Entered instance of PyMimeData")
                if self._local_instance is not None:
                    return self._local_instance

                io = StringIO(str(self.data(self.MIME_TYPE)))

                try:
                    # Skip the type.
                    load(io)

                    # Recreate the instance.
                    return load(io)
                except:
                    print("load failed - instance - PyMimeData")
                    pass

                return None

            def instanceType(self):
                print("entered instanceType")
                """ Return the type of the instance.
                """
                if self._local_instance is not None:
                    return self._local_instance.__class__

                try:
                    return loads(str(self.data(self.MIME_TYPE)))
                except:
                    print("instanceType, load failed.")
                    pass

                return None

            ''' 
            Note.  TreeItem was built subclassing Qobject.  Then at the last it was converted to subclass QStandardItem.   
            Most likely it could be simplified.
            Some methods may need to renamed to over write QStandardItem methods that accomplish the same thing.
            '''

        from PyQt5 import QtCore, QtWidgets
        from PyQt5.QtWidgets import *
        from PyQt5.QtGui import *
        from PyQt5.QtCore import *
        from PyQt5.QtCore import QVariant
        from pickle import *
        import photo_database_code
        from photo_database_code import *

        SortRole = Qt.UserRole + 1

        class PyMimeData(QMimeData):
            """ The PyMimeData wraps a Python instance as MIME data.
            """
            # The MIME type for instances.
            # MIME_TYPE = QString('application/x-ets-qt4-instance')
            MIME_TYPE = 'application/x-ets-qt5-instance'  # maybe qt5

            def __init__(self, data=None):
                """ Initialise the instance.
                """
                # Required
                QMimeData.__init__(self)

                # Keep a local reference to be returned if possible.
                self._local_instance = data

                if data is not None:
                    # We may not be able to pickle the data.
                    try:
                        pdata = dumps(data)
                    except:
                        return

                    # This format (as opposed to using a single sequence) allows the
                    # type to be extracted without unpickling the data itself.
                    self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)
                print("exiting __init__ of pymimedata")

            @classmethod
            def coerce(cls, md):
                """ Coerce a QMimeData instance to a PyMimeData instance if
        possible.
                """
                # See if the data is already of the right type.  If it is then we know
                # we are in the same process.
                print("In classmethod - PyMimeData")
                if isinstance(md, cls):
                    return md

                # See if the data type is supported.
                if not md.hasFormat(cls.MIME_TYPE):
                    return None

                nmd = cls()
                nmd.setData(cls.MIME_TYPE, md.data())

                return nmd

            def instance(self):
                """ Return the instance.
                """
                print("Entered instance of PyMimeData")
                if self._local_instance is not None:
                    return self._local_instance

                io = StringIO(str(self.data(self.MIME_TYPE)))

                try:
                    # Skip the type.
                    load(io)

                    # Recreate the instance.
                    return load(io)
                except:
                    print("load failed - instance - PyMimeData")
                    pass

                return None

            def instanceType(self):
                print("entered instanceType")
                """ Return the type of the instance.
                """
                if self._local_instance is not None:
                    return self._local_instance.__class__

                try:
                    return loads(str(self.data(self.MIME_TYPE)))
                except:
                    print("instanceType, load failed.")
                    pass

                return None

            ''' 
            Note.  TreeItem was built subclassing Qobject.  Then at the last it was converted to subclass QStandardItem.   
            Most likely it could be simplified.
            Some methods may need to renamed to over write QStandardItem methods that accomplish the same thing.
            '''

        self.treeView = parent
        self.headers = ['Item', 'State', 'Description']

        self.columns = 3

        # Create items
        self.root = myNode('root', 'on', 'this is root', None)

        itemA = myNode('itemA', 'on', 'this is item A', self.root)
        itemA1 = myNode('itemA1', 'on', 'this is item A1', itemA)

        itemB = myNode('itemB', 'on', 'this is item B', self.root)
        itemB1 = myNode('itemB1', 'on', 'this is item B1', itemB)

        itemC = myNode('itemC', 'on', 'this is item C', self.root)
        itemC1 = myNode('itemC1', 'on', 'this is item C1', itemC)

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)

        if index.isValid():
            return Qt.ItemIsEditable | Qt.ItemIsDragEnabled | \
                   Qt.ItemIsDropEnabled | defaultFlags

        else:
            return Qt.ItemIsDropEnabled | defaultFlags

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

    def mimeTypes(self):
        types = QStringList()
        types.append('application/x-ets-qt4-instance')
        return types

    def mimeData(self, index):
        node = self.nodeFromIndex(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True

        dragNode = mimedata.instance()
        parentNode = self.nodeFromIndex(parentIndex)

        # make an copy of the node being moved
        newNode = deepcopy(dragNode)
        newNode.setParent(parentNode)
        self.insertRow(len(parentNode) - 1, parentIndex)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                  parentIndex, parentIndex)
        return True

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()

        return True

    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        return self.createIndex(row, column, node.childAtRow(row))

    def data(self, index, role):
        if role == Qt.DecorationRole:
            return QVariant()

        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))

        if role != Qt.DisplayRole:
            return QVariant()

        node = self.nodeFromIndex(index)

        if index.column() == 0:
            return QVariant(node.name)

        elif index.column() == 1:
            return QVariant(node.state)

        elif index.column() == 2:
            return QVariant(node.description)
        else:
            return QVariant()

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        node = self.nodeFromIndex(child)

        if node is None:
            return QModelIndex()

        parent = node.parent

        if parent is None:
            return QModelIndex()

        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)

        assert row != - 1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.root

