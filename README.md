# DragDropTreeWithAbstractItemModel
PyQt TreeView with AbstractItemModel with Drag and Drop and SQL Data Source
Getting a full blown TreeView linked to an implementtion of QAbstractItemModel has been an effort.
Lots of snippets and limited models.  But no complete project that I could learn from. So I thought I would put this up so maybe others can learn.

Also since I am new to Python others might improve and I can learn from that.  My last programing projects were in the early 1990's before Windows. 
Needless to say a lot has changed.  And given that this is an early effort I will not be surprised if there are better ways.

I need a hierarchical tree that can be unlimited depth.  More accuractely I have no idea how deep the data will take me, so my code has to be able
to handle unlimited depth.   I need to be able drag and drop items to rearrange the tree.  And then save those changes back to the underlying database.
The initial data comes in from external sources and may or may not be properly arranged in hierarchical order, so a users first task maybe to straighten
out the tree.

I also need to be able to drag and drop items from the tree onto ojects in another part of the display.  This will link those objects to the items in the tree. 
Tag them.

I need dragging and dropping to be much more robust than dragging one item at a time.  I need to be able copy entire nodes with multiple levels of children.  
I need to be able to copy multiple childless items at a time to the same spot.  This code so far can do that and also copy multiple sibling child containing nodes
to a new spot.   At present there is still a problem with copying dragging nodes with children and siblings without children at the same time.

While I only display the name of the item, it is part of a tuble that has it row from the SQL database and its SQL parent. I need this information for both the 
tagging and SQL database reparenting.  I was unable to do this initially using QstandardItem objects for the tree Items.  Just before completing this I changed TreeItem
to be based on QStandardItem rather than Qobject.  To my surprise it seems to work, so this will allow some rework of the code eventually.
