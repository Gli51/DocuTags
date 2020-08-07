DOCUTAGS (15-112 Summer 2020)
=========================================================================

HOW TO RUN:
Docutags should run out of the box.

=========================================================================

FILE I/O NOTES:
Launching the app will create a directory in the local folder called "docfiles".

Any files created in the app will be sent to this folder.
Additionally, when deleting files, the files will be deleted from that folder.
By default, the filename will be set to the title name of your book.
Thus, it is encouraged not to use special characters when naming your documents in the app.

DOCUMENTS ADDED TO THE "DOCFILES" DIRECTORY CAN BE LOADED IN IF THEY MEET THE FOLLOWING SPECIFICATIONS:

Contains lines that begin with (/) and then one each of:
Title:
Doctags:
Pages:
Pagetags:

Tags in Doctags are separated by commas. 
Page content in Pages are separated by <pwords>.
Each grouping of tags in Pagetages are separated by <tname>.

EXAMPLE FILE CONTENTS BELOW:

(/)Title: Fire and Ice
(/)Doctags: robert frost
(/)Pages: Some say the world will end in fire,
Some say in ice.
From what I've tasted of desire
I hold with those who favor fire.
But if it had to perish twice,
I think I know enough of hate
To say that for destruction ice
Is also great
And would suffice.<pwords>The end
(/)Pagetags: poems,short<tname>len = 2