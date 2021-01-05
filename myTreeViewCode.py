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
    ''' This class is pretty much as I found it.  However all of the stuff
    about serializing the data does not work.  The TreeItem indexes passed along by the
    start Drag functions can not be serialized.
    
    This module works because 1) We are draging and dropping within the same program
    and 2)  It perserves a copy of the data here in the INSTANCE variable.  On drop we then
    retrieve that data.
    '''




    MIME_TYPE = 'application/x-ets-qt5-instance'  # maybe qt5

    def __init__(self, data=None):
        """ Initialise the instance.
        """
        # Required
        QMimeData.__init__(self)

        # Keep a local reference to be returned if possible.
        # it because we do this that this class works at all.  The tree items
        # can not be pickled.  At least as they stand now.  I believe some methods can
        # be added to the TreeItem class so they cn be serialized.

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
        # print("Entered instance of PyMimeData")
        if self._local_instance is not None:
            return self._local_instance
        # This is where we get the mimedata back on dropping.


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


class TreeItem(QStandardItem):

    def __init__(self, data, parent=None):
        # required
        super(TreeItem, self).__init__(parent)
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
        # set default setting
        self.DropEnabled = False                # this is needed because we are rolling our own Class, Pre QStandardItem
        self.Checkstatus = Qt.Unchecked         # this is needed because we are rolling our own Class basee on QObject.

    def appendChild(self, child):
        # required - loads initial data
        # from drag drop model
        self.childItems.append(child)

    def child(self, row):
        # required
        # from simple and editable examples
        return self.childItems[row]

    def childCount(self):
        # required
        # from simple and editable examples
        return len(self.childItems)

    def columnCount(self):
        # required
        return len(self.itemData)

    def data(self, column):
        # Required
        # from simple and editable models
        try:
            return self.itemData[column]
        except IndexError:
            print("Index Error - data in Tree Item")
            return None

    def insertChildren(self, data, position, rowcount, columns, acceptdrops):
        # from editable model
        # required
        # Added acceptdrops to standard prototypes, as we need this set for nodes with children (containers) to make
        # Drag and Drop more intuitive.  People expect to be able to drop ONTO containers.
        if position < 0 or position > len(self.childItems):
            return False
        for row in range(rowcount):  # row count is always 1 in our model.
            item = TreeItem(data, self)
            item.DropEnabled = acceptdrops
            self.childItems.insert(position, item)
        return True

    def parent(self):
        # Required
        # from simple and editable model
        return self.parentItem

    def removeChildren(self, position, count):
        # from editable model
        # required
        if position < 0 or position + count > len(self.childItems):
            return False
        for row in range(count):
            self.childItems.pop(position)
        return True

    def removeChild(self, row):
        # required
        # from drag drop model
        value = self.childItems[row]
        self.childItems.remove(value)
        return True

    def row(self):
        # required
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def setDropEnabled(self, value):
        # required
        self.DropEnabled = value

    def isDropEnabled(self):
        # required
        # this makes drop Enabled dynamic.  If it has children Yes, otherwise no.  help in drag and drop creation of new items.
        if len(self.childItems) > 0:
            return True
        else:
            return False

    def checkboxstate(self):
        # required if you want check boxes
        # because we are rolling our own treeitem class
        return self.Checkstatus

    def setcheckboxstate(self, value):
        # required if you want check boxes
        self.Checkstatus = value
        return True

    '''  Items below this point are most likely not needed
         in this implementation.  May be need in others, especially those that use columns   
         After full confirmaton removed '''

    def __len__(self):
        # print(len(self.childItems))
        return len(self.childItems) + 1

    def childAtRow(self, row):
        # from Drag Drop Model
        # looks to be duplicate of Child.
        print("Entered ChildAtRow - Tree Item")
        return self.childItems[row]

    def childNumber(self):
        print("Entered Child number - Tree Item")
        print(self)
        # from simple and editable examples
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)

    def insertColumns(self, position, columns):
        print("In insert column,- treeItem")
        # from editable model
        # this is likely not used in our setup
        if position < 0 or position > len(self.itemData):
            return False
        for column in range(columns):
            self.itemData.insert(position, None)
        for child in self.childItems:
            child.insertColumns(position, columns)
        return True

    def removeColumns(self, position, columns):
        print("In RemoveColumns - TreeItem")
        # from editable model
        # likely not used in our set up
        if position < 0 or position + columns > len(self.itemData):
            return False
        for column in range(columns):
            self.itemData.pop(position)
        for child in self.childItems:
            child.removeColumns(position, columns)
        return True

    def setData(self, column, value):
        # from editable model
        print("Entered setData in TreeItem")
        if column < 0 or column >= len(self.itemData):
            return False
        self.itemData[column] = value
        return True


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, headers, data, mydb, parent=None):
        super(TreeModel, self).__init__(parent)
        self.mydb = mydb  # preserve database object so it can be accessed and passed down.
        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)  # this is required because setupModelData needs a parent.
        self.rootItem.setDropEnabled(False)
        self.setupModelData(data, self.rootItem)
        self.columns = 4
        print("exiting TreeModel __init__")

    def columnCount(self, parent):
        # Required
        # from Simple tree model, similar to Editable tree model
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role=None):
        # required
        #  This is good place to see how ROLES really work.
        row = index.row()
        column = index.column()
        if role == Qt.DecorationRole:
            # print("Decoration role requested")
            return None
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))
        if not index.isValid():
            print("invalid index data request")
            return None
        item = self.getItem(index)
        if role == SortRole:
            # print("Sort Role requested")
            # print(item.data(2))
            return item.data(2)
        if role == Qt.CheckStateRole and column == 0:
            return item.checkboxstate()
        if role != Qt.DisplayRole:
            # print("non Disply role requested" + str(role))
            return None
        temp = item.data(index.column())
        return temp

    def flags(self, index):
        # required
        node = self.nodeFromIndex(index)
        defaultFlags = QAbstractItemModel.flags(self, index)  # from drag drop model
        if not index.isValid():
            # print("index is not valid - flags - TreeModel")
            return defaultFlags  # returning a valid flag keeps things from crashing.
        if node.isDropEnabled():
            # return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | defaultFlags
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | defaultFlags
        else:
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | defaultFlags

    def getItem(self, gtindex):
        # required
        # from editable model
        if gtindex.isValid():
            item = gtindex.internalPointer()
            if item:
                return item
        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # required
        # from Simple tree model and editable model
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent=QModelIndex()):
        # required
        # from editable model
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()
        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def insertRow(self, data, row, parent, acceptdrops = False):
        # required
        # from drag Drop model
        print(type(data))
        return self.insertRows(data, row, 1, acceptdrops, parent)

    def insertRows(self, data, position, rows, acceptdrops, irparentindex=QModelIndex()):
        # Required
        # from editable model
        parentItem = self.getItem(irparentindex)
        self.beginInsertRows(irparentindex, position, position + rows - 1)
        success = parentItem.insertChildren(data, position, rows, self.rootItem.columnCount(), acceptdrops)
        self.endInsertRows()
        return success

    def nodeFromIndex(self, index):
        # Required
        # From Drag Drop Model
        return index.internalPointer() if index.isValid() else self.rootItem

    def parent(self, index):
        # Required
        # from simple tree model and editable model index
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem = self.getItem(index)
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def removeRows(self, position, rows, parent=QModelIndex()):
        # required
        # from editable model
        parentItem = self.getItem(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()
        return success

    def rowCount(self, parent=QModelIndex()):
        # required
        # From Simple tree model
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            rcparentItem = self.rootItem
        else:
            rcparentItem = self.getItem(parent)
        return rcparentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
        # required
        # from editable model
        # reviewed
        item = self.getItem(index)
        if role == Qt.EditRole:
            result = item.setData(index.column(), value)
            self.dataChanged.emit(QModelIndex(), index)  # Let the world know we update the View.
        elif role == Qt.CheckStateRole:
            result = item.setcheckboxstate(value)
            self.dataChanged.emit(QModelIndex(), index)  # Let the world know we update the View.
        else:
            return False
        if result:
            self.dataChanged.emit(index, index)
        return result

    '''  items below are for drag and drop'''

    def supportedDropActions(self):
        # required
        # from drag drop model
        return Qt.CopyAction | Qt.MoveAction

    def mimeTypes(self):
        # required.
        # From Drag Drop model
        types = []
        types.append('application/x-ets-qt5-instance')
        return types

    def mimeData(self, indices):
        #  required
        # from drag drep model
        print("Enetered mimeData - TreeModel")

        node = self.nodeFromIndex(indices[0])
        mimeData = PyMimeData(indices)
        print(type(mimeData))
        print(mimeData)
        return mimeData

    def canDropMimeData(self, data, action: Qt.DropAction, row: int, column: int, parent: QModelIndex) -> bool:
        # required
        droptarget = self.nodeFromIndex(parent)
        dropok = droptarget.isDropEnabled()
        print(dropok)
        return dropok

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        # from drag drop model
        # print("Entered drop MimeData")
        # print("Target Row is " + str(row))
        print("Drop MimeData Action " + str(action))
        if row == -1:  # this means we are dropping ONTO the target, not below so insert at top of list.
            row = 0
        if action == Qt.IgnoreAction:
            print("returned for Ignore Action")
            return True
        dragNode = mimedata.instance()
        index = len(dragNode) - 1
        result = True
        dragNodeParent = None
        while index >= 0:
            onenode = self.nodeFromIndex(dragNode[index])
            if dragNodeParent == None:
                dragNodeParent = onenode.parentItem  # populates with first item processed
            if dragNodeParent is not onenode.parentItem:
                index -= 1
                continue  # discard this item and go back for more
            oneresult = self.dropManyRows(onenode, row, parentIndex)  # takes a node, not an index
            index -= 1
            if not oneresult:
                result = False

        return result

    def dropManyRows(self, dragNode, row, parentIndex, result=True):
        newdata = dragNode.itemData
        newparent = self.nodeFromIndex(parentIndex)
        if dragNode.childCount() > 0:
            # dragging a container with children
            childresult = self.dropOneRow(newdata, row, parentIndex,
                                          True)  # process the parent node, should accept drops
            if childresult == None:
                print("drop one Row failed in Drop many Rows")
                result = False
            # now update the underlying database
            db_row_to_update = newdata[1]
            newparent_row = newparent.itemData[1]
            self.mydb.update_parent_tag(db_row_to_update,
                                        newparent_row)  # We only need to update database for top item in move
            # now setup to process the child nodes
            dragchilds = dragNode.childItems
            for childnode in dragchilds:
                if childnode.childCount() > 0:
                    childresult2 = self.dropManyRows2(childnode, 0, childresult, result)  # We are going Two levels deep
                    if childresult2 == None:
                        print("Drop Many rows 2 returned False")
                        result = False
                else:
                    childdata = childnode.itemData
                    childresultx = self.dropOneRow(childdata, 0, childresult)  # also insert into row 0 Model will sort
                    if childresultx == None:
                        result = False  # If any opertion fails then whole move fails
            return result
        else:
            dropresult = self.dropOneRow(newdata, row, parentIndex)
            if dropresult == None:
                result = False
            # now update the underlying database
            db_row_to_update = newdata[1]
            newparent_row = newparent.itemData[1]
            self.mydb.update_parent_tag(db_row_to_update,
                                        newparent_row)  # We only need to update database for top item in move
            return result

    def dropManyRows2(self, dragNode, row, parentIndex, result):
        print("in Drop Many TWO")
        newdata = dragNode.itemData
        if dragNode.childCount() > 0:
            childresult = self.dropOneRow(newdata, row, parentIndex, True)
            if childresult == None:
                result = False
                print("drop one failed in Drop Many 2")
            dragchilds = dragNode.childItems
            for childnode in dragchilds:
                if childnode.childCount() > 0:
                    childresultz = self.dropManyRows2(childnode, 0, childresult,
                                                      result)  # we are going three or more levels deep
                    if childresultz == None:
                        result = False
                else:
                    childdata = childnode.itemData
                    childresultx = self.dropOneRow(childdata, 0, childresult)  # also insert into row 0 Model will sort
                    if childresultx == None:
                        print("drop one failed in Dropmanyrows 2 -xxx")
                        result = False  # If any opertion fails then whole move fails
            return result
        else:
            childresult = self.dropOneRow(newdata, row, parentIndex)
            if childresult == None:
                result = False
            return result

    def dropOneRow(self, newdata, row, dpparentIndex, acceptdrop=False):
        # required
        result = self.insertRow(newdata, row, dpparentIndex)  # this inserts the row into the Model
        self.dataChanged.emit(QModelIndex(), dpparentIndex)  # Let the world know we update the Model
        if result:
            # we need to create an index that point to the object just created, in case this a container row.
            newitemhasindex = self.hasIndex(row, 0, dpparentIndex)
            if newitemhasindex:
                newitemindex = self.index(row, 0, dpparentIndex)
                if newitemindex.isValid():
                    return newitemindex
                else:
                    print("invalid index created in drop one row")
            else:
                print("DropOnerow, new items does not have an index")
        else:
            print("Insert Row failed in dropOneRow")
        return

    def setupModelData(self, data2, root):
        # required for my implementation.
        # this is unique to this implementation,  Every implematation will need it own way of loading data into model
        # This loads loads the model with the data from the SQL Query
        seen = {}  # dictionary of row objects that have been inserted.
        # we can not load a row unless the parent has already been inserted.  This keeps track of what has been inserted.
        while data2:
            row = data2.pop(0)
            if row[1] == 0:  # Level data - unique to my data
                parent = root  # parent is a standard TreeItem object
            else:
                parent_id = row[4]  # Parent ID in tag table
                if parent_id not in seen:  # cannot insert child if parent not present
                    data2.append(row)  # add it back on list to  imported
                    continue  # circle back around for next item
                parent = seen[parent_id]  # model row item object of parent
            database_id = row[0]  # tag database row id  the row of source data
            #        new_data = {row[3], row[0]}
            if row[1] == 0:  # Level - Base
                # parent.appendRow([QStandardItem(row[3])])
                print("inserting base row")
                # print(row[2])
                treedata = (row[3], str(row[0]), row[7], str(row[4]))
                treedataobj = TreeItem(treedata, parent)
                treedataobj.setDropEnabled(True)
                # treedataobj.setCheckable(True)
                parent.appendChild(treedataobj)

            else:
                # parent.appendRow([QStandardItem(row[3])])   -- original row with just one item - save in notes
                treedata = (row[3], str(row[0]), row[7], str(row[4]))
                treedataobj = TreeItem(treedata, parent)  # this will append item into tree
                if row[2] == 0:  # is not group row, ie no children
                    # treedataobj.setCheckState(False)
                    # treedataobj.setCheckable(True)
                    treedataobj.setDropEnabled(False)  # items which are not groups should not accept drops.
                    # treedataobj.setDragEnabled(False)
                    # item_id.setDropEnabled(False)
                    # treedataobj.setData(str(row[0]), Qt.DisplayRole)
                else:
                    treedataobj.setDropEnabled(True)
                parent.appendChild(treedataobj)
            seen[database_id] = treedataobj
        print("all tags imported")

        """  Stuff below this line does not appear to be required in my installation
             They were taken from various models that went into this implementation
             and may have been needed at one time.

             Some appear to be for moving columns such as in table views so are left
             here for others to look at

        """

    def insertColumns(self, position, columns, parent=QModelIndex()):
        print("Entered insertColumns - TreeModel")
        # reviewed
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()
        return success

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        print("Entered setHeaderData - Tree Model")
        # reviewed
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False
        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)
        return result

    def removeColumns(self, position, columns, parent=QModelIndex()):
        print("removeColumns - TreeModel ")
        # from editable model
        # reviewed.
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()
        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())
        return success

    def removeRow(self, row, parentIndex=QModelIndex()):
        # from drag Deop Model
        print("in Remove Row")
        return self.removeRows(row, 1, parentIndex)


class myTreeView(QTreeView):

    def __init__(self, parent=None):
        super(myTreeView, self).__init__(parent)
        mydbpath = photo_database_code.create_data_dir()
        myphotodatabase = PhotoDatabase(mydbpath)
        self.mydb = myphotodatabase
        print("database to be used is " + myphotodatabase.database)
        myphotodatabase.connect()
        curr = myphotodatabase.cursor
        sq = "Select * from tags ORDER BY TagClass, level, tag"
        myphotodatabase.execute(sq)
        data2 = curr.fetchall()
        print(len(data2))
        myphotodatabase.close_database()
        headers = ("Tag", "Database Row", "Sort Column", "DB Parent Row")
        # proxy sortfilter stuff
        sourceModel = TreeModel(headers, data2, myphotodatabase)
        proxyModel = QSortFilterProxyModel()
        proxyModel.setSortRole(SortRole)
        proxyModel.setSourceModel(sourceModel)
        self.setModel(proxyModel)
        self.setSortingEnabled(True)
        self.sortByColumn(2, Qt.AscendingOrder)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.showDropIndicator()
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.expandToDepth(1)
        self.setHeaderHidden(True)
        self.resizeColumnToContents(0)
        self.setColumnHidden(3,True)  # hide all the columns we do not want to show.
        self.setColumnHidden(2,True)  # these columns carry data we need elsewhere
        self.setColumnHidden(1,True)
        self.setUniformRowHeights(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # otherwise the built in edit of items happens, model doesn't handle this
        self.setExpandsOnDoubleClick(True) #  only works if edit triggers is off
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows) # must be this for our implementation, other setting disable delete in drag and drop
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)

        self.setAnimated(True)
        self.setAllColumnsShowFocus(True)

    def change(self, topLeftIndex, bottomRightIndex):
        print("Entered Change in TreeView")
        self.update(topLeftIndex)
        self.expandAll()
        self.expanded()

    def expanded(self):
        print("Entered Expanded in TreeView")
        for column in range(self.model().columnCount(QModelIndex())):
            self.resizeColumnToContents(column)
