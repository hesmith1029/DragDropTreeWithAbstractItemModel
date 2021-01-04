from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QVariant
from pickle import *
import photo_database_code
from photo_database_code import *


SortRole = Qt.UserRole + 1
# this is a changes

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
