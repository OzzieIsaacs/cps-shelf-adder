## How to use

Create a list of books to add to a shelf by exporting it from calibre (Menu convert books, create catalog of books in library)
Select csv as format, select in options which coloums to export. The coloum 'id' has to be exported everythng else is optional. 
Please make sure that every line in the exported file contains a id, exporting comments and other long texts is therefore not recommended.
Open the file in the editor and delete all lines which shall not be added to the shelf and save it. 
Important: The items (if more than the id is exported) have to be comma seperated, otherwise the import won't function.

Open the file mass_add_books.py, set the parameters to the right values. The id of the shelf can be found out in the browser, 
by moving with the mouse over the add to shelf element, the id of the shelf is displayed in the adress shown. Booklist is the filename from above.

username = 'admin'

password = 'admin123'

shelf_id = '1'

booklist = 'booklist.csv'

serveradress = 'http://127.0.0.1:8083'

Make sure calibre-web is running, and start the script: python mass_add_books.py

Done
