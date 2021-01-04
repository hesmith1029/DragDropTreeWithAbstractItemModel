# DragDropTreeWithAbstractItemModel
PyQt TreeView with AbstractItemModel with Drag and Drop and SQL Data Source.  
Getting a full-blown TreeView linked to an implementation of QAbstractItemModel has been an effort. 
Lots of snippets and limited models, but no complete project that I could learn from. So I thought I would put this up
so maybe others can learn.

Also since I am new to Python, others might be able to improve this code. I can learn from that.  My last programing
projects were in the early 1990's before Windows. Needless to say a lot has changed.  Given that this is an early
effort I will not be surprised if there are better ways.

I need a hierarchical tree that can be of unlimited depth.  More accurately I have no idea how deep the data will
take me, so my code has to be able to handle unlimited depth.  I need to be able to drag and drop items to rearrange
the tree.  Then save those changes back to the underlying database.  The initial data comes in from external sources 
and it may or may not be properly arranged in hierarchical order, so a users first task may be to straighten out 
the tree.

I also need to be able to drag and drop items from the tree onto objects in another part of the display.  This will
link those objects to the items in the tree.  Tag them.  I need access to more than just the display name when 
doing this I need the SQL row number that is part the TreeItem data.

I need dragging and dropping to be much more robust than dragging one item at a time. We will be dealing with thousands
of items.  I need to be able to copy entire nodes with multiple levels of children.  I need to be able to copy multiple
childless items at a time to the same spot.  This code so far can do that and also copy multiple sibling child
containing nodes to a new spot.  At present there is still a problem with copying dragging nodes with children and
siblings without children at the same time.

I have implemented sorting.  In the sample database attached you will a sort column.  I pre-appended a string to the
item name if the item was container.  This forces a sort order I prefer, you may choose something different.  Ideally
this sorting should be handled in the Proxy Model, but that is for a later time.

While I only display the name of the item, it is part of a tuple that has data about the row from the SQL database
and its SQL parent. I need this information for both the tagging and SQL database re-parenting.  I was unable to do 
this initially using Qstandarditem objects for the tree Items. Most of the samples I worked from based TreeItem on
QObject.  Just before completing this I changed TreeItem to be based on QStandardItem rather than Qobject.  
To my surprise it seems to work, so this will allow some rework of the code eventually.  

The samples this work is based on had references for doing work on columns.  These have been left in, but they are
not used in my implementation.  If you have a table rather than a TreeView, they might be useful.
