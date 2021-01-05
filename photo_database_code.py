import sqlite3
import os.path


class PhotoDatabase:
    """This database holds all the pointers to photos orig and thumbs.  It also holds all the tag info"""

    def __init__(self, db_location):
        super(PhotoDatabase, self).__init__()
        # db_location is guaranteed to exist by prior call to create data dir in main code.
        # print("Start of init " + db_location)
        self.connected = False
        self.database = db_location + "\\EnjoyYP.db"
        # this will connect to database, but also create empty database if it does not exist
        self.connect()

        print("we are now connected to database")
        #  Check status of database and create and initialize if needed
        self.create_tables()            # This creates tables if the do not exist.  Also seeds tags table.

        # statements verify or create new database go here
        self.close_database()        # close up database and reopen each time needed.

    def dbnametest(self):
        return self.database

    def connect_status(self):
        return self.connected

    def connect(self):
        # This makes the actual connection

        # print("Connecting to database")
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connected = True

    def close_database(self):
        # this closes up the database
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def execute(self, new_data):
        # print("Entering execute in photo database code")
        if not self.connected:
            print("Database not connected, connecting now")
            self.connect()

        # print("command being executed is " + new_data)
        # print(self.cursor.rowcount)
        self.cursor.execute(new_data)

    def executemany(self, many_new_data):
        # needs code
        return

    def fetchallxx(self):
        # print("in fetch all")
        datalist = self.cursor.fetchall()
        # print("In Fetchall")
        return datalist

    def fetch(self, fetch_cmd):
        # print("in fetch one")
        # execute the command then get first row of data.
        self.cursor.execute(fetch_cmd)
        datalist = self.cursor.fetchone()
#        print("printing datalist next")
#        print(datalist)
        return datalist

    def create_tables(self):
        print("In create table")
        # A connection is guaranteed to exist at this point
        table_photo_def = "CREATE TABLE IF NOT EXISTS Photos (photonum integer PRIMARY KEY AUTOINCREMENT, " \
            "photoname TEXT NOT NULL, photopath TEXT, photodate TEXT, dateTimeOriginal TEXT, " \
            "documentID TEXT NOT NULL UNIQUE, instanceID TEXT,originalDocumentID TEXT, thumbexist INT )  ; "
        try:
            # print("Table Photos created or exists")
            self.execute(table_photo_def)
        except Exception as err:
            print(err)
            print("error creating Photo table")
            # Needs an error hander here,  Message display????
        self.commit()
        # now set up TagLink table

        table_link_def = "CREATE TABLE IF NOT EXISTS TagLink (documentID TEXT NOT NULL, TagPointer INTEGER NOT NULL) ; "

        try:
            # print("TagLink exists or is being created")
            self.execute(table_link_def)
        except Exception as err:
            print(err)
            print("error creating taglink table")
        self.commit()
        table_tag_def = "CREATE TABLE IF NOT EXISTS Tags (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "level INTEGER NOT NULL, isGroup INTEGER NOT NULL, tag TEXT NOT NULL, " \
                        "parentID INTEGER NOT NULL, Deletable INTEGER NOT NULL DEFAULT 'True', TagClass TEXT, " \
                        "SortCode TEXT, Description TEXT) ; "
        try:
            # main_window.db_status_bar.statusbar.showMessage("Creating tags table")
            # print("Table TAGS created or exists")
            self.execute(table_tag_def)
        except Exception as err:
            print(err)
            print("error creating Tags table")
            # Needs some error handling here.  Display message then quit???
        self.commit()
        # now we need to see if tags is new ie empty, if so insert initial base rows.
        tag_new_query = "SELECT * FROM Tags"
        tag_rows = self.fetch(tag_new_query)
        if tag_rows is None:
            # database is empty
            # need to add the 4 base (default) tag catagories.
            print("tag database is empty")
            sqlcmd = "INSERT INTO tags (Level, isGroup, Tag, parentID, Deletable, TagClass, SortCode, Description) " \
                     " VALUES (0,1,'People',0,'False','Base', 'AAAAAA', 'Base object for People Tags'); "
            self.execute(sqlcmd)
            sqlcmd = "INSERT INTO tags (Level, isGroup, Tag, parentID, Deletable, TagClass, SortCode, Description) " \
                     "VALUES (0,1,'Location',0,'False','Base', 'AAAAAB', 'Base object for Location Tags'); "
            self.execute(sqlcmd)
            sqlcmd = "INSERT INTO tags (Level, isGroup, Tag, parentID, Deletable, TagClass, SortCode, Description) " \
                     "VALUES (0,1,'Events',0,'False','Base', 'AAAAAC', 'Base object for Event Tags'); "
            self.execute(sqlcmd)
            sqlcmd = "INSERT INTO tags (Level, isGroup, Tag, parentID, Deletable, TagClass, SortCode, Description) " \
                     "VALUES (0,1,'Status',0,'False','Base', 'AAAAAD', 'Base object for Status Tags'); "
            self.execute(sqlcmd)

        else:
            pass
            # print("Tag database has data")
        return

    def commit(self):
        self.connection.commit()

    def update_parent_tag(self, tag_row=None, new_parent=None):
        # print("Reached update parent tag")
        self.connect()
        sq = "UPDATE tags SET parentID = " + str(new_parent) + " WHERE id = " + str(tag_row) + " ;"
        self.execute(sq)
        self.commit()


# Not part of the class.
# But put code here to keep in a logical place.  Unclutter main.


def create_data_dir(photo_data_path=None):
    # print("reached create database directory")

    if photo_data_path is None:
        photo_data_path = os.getcwd() + "\\data"

    if not os.path.isdir(photo_data_path):
        try:
            os.mkdir(photo_data_path)
            print("making DATA directory")
        except Exception as err:
            print(err)
            print("failed to create DATA directory")

    # now do the same for thumbs.
    thumb_dir = photo_data_path + "\\thumbs"
    print(thumb_dir)
    if not os.path.isdir(thumb_dir):
        try:
            os.mkdir(thumb_dir)
            print("making THUMBS directory")
        except Exception as err:
            print(err)
            print("Failed to create THUMBS directory")
    return photo_data_path
