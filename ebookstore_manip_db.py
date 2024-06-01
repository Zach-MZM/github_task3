import sqlite3
import os

# creates or opens ebookstore database
if not os.path.exists("database/ebookstore.db"):
    db = sqlite3.connect("ebookstore.db")
else:
    db = sqlite3.connect("database/ebookstore.db")    

# cursor object to modify database through sql commands
cursr = db.cursor() 
if not os.path.exists("database"):
    try:
        cursr.execute('''CREATE TABLE book(
        id int(4) NOT NULL,
        title varchar(255),
        author varchar(255),
        qty int(4));
        ''')
    except:
        pass

#enters initial ebook data to the database

    #https://stackoverflow.com/questions/1912095/how-to-insert-a-value-that-contains-an-apostrophe-single-quote
    try:
        cursr.execute('''INSERT INTO book
        VALUES(3001,'A Tale of Two Cities','Charles Dickens',30),
        (3002,'Harry Potter and the Philosopher''s Stone','J.K. Rowling',40),
        (3003,'The Lion, the Witch and the Wardrobe','C. S. Lewis',25),
        (3004,'The Lord of the Rings','J.R.R Tolkien',37),
        (3005,'Alice in Wonderland','Lewis Carroll',12);
        ''')
        db.commit() 
    except:
        pass

    os.mkdir("database")
    os.system("mv ebookstore.db database")

def format_data(listed_data):
    '''formats the listed data in a readable format'''
    compiled_lines = "  id|title|author|qty "

    # iterates through the listed tuples, organizes the data 
    # in a data|data layout and appends to compiled_lines 
    for data in listed_data:
        layout = f"\n{data[0]}|{data[1]}|{data[2]}|{data[3]}"
        compiled_lines += layout
    return compiled_lines

def add_book_db():
    '''adds new books to the database'''
    
    title = input("\n\nWhat is the title of the book? ")
    author = input("\n\nWho is the primary author of the book? ")
    try:
        qty = int(input("\n\nHow many books are being registered? "))
        
        contents = cursr.execute('''SELECT * FROM book''')
        print(format_data(contents.fetchall()))
        
        # determines recent entry id and updates it for the new entry
        id = cursr.execute('''SELECT MAX(id) FROM book''')
        id = id.fetchone()[0]
        new_id = id + 1
        
        # adds new record to the database
        cursr.execute('''INSERT INTO book
        VALUES(?,?,?,?)
        ''',(new_id, title, author, qty))


        # saves the changes to the database
        db.commit()
        contents = cursr.execute('''SELECT * FROM book''')
        print(format_data(contents.fetchall()))
    except:
        print("ValueError")

def update_book():
    '''updates book information'''

    # returns the records of the book table
    contents = cursr.execute('''SELECT * FROM book''')
    print(format_data(contents.fetchall()))
    
    # gets all id values from column
    ids = cursr.execute('''SELECT id FROM book''')
    
    # returns tuple values in list format
    ids = ids.fetchall()
    
    # selects first value from each tuple in the list
    ids = [str(id[0]) for id in ids]
    id = input("\nWhat is the book id? ")
    
    if id in ids:
        # selects id column and displays specified book id record
        contents = cursr.execute('''SELECT * FROM book 
        WHERE id = ?''',(id,))
        print(contents.fetchone())

        # provides selection options for editing book record
        try:
            edit_selection = int(input(
            "\nEnter 1 to edit the title, 2 to edit the author, or 3 to edit the quantity: "))
            edit_options = ['title','author','qty']
        
            if edit_selection == 1 or edit_selection == 2 or edit_selection == 3:

                # assigns selection to be modified based on user input
                edit_selection = edit_options[edit_selection-1]
                
                edit = input("Please provide your new entry: ")
                
                # updates selected option in the book record based on provided book id
                cursr.execute(f'''UPDATE book
                SET {edit_selection} = ?
                WHERE id = ?''',(edit, id))

                # displays updated book record
                contents = cursr.execute('''SELECT * FROM book
                WHERE id = ?''', (id,))
                print(contents.fetchone())

                # completes the transaction
                db.commit()
    
            else:
                print("Entry does not exist.")
        except: 
            print("ValueError")

    else:
        print("Entry does not exist.")
        

    db.commit()

def delete_book():
    '''deletes books from the database'''
    
    # returns the records of the book table
    contents = cursr.execute('''SELECT * FROM book''')
    print(format_data(contents.fetchall()))
    
    # gets all id values from column
    ids = cursr.execute('''SELECT id FROM book''')
    
    # returns tuple values in list format
    ids = ids.fetchall()
    
    # selects first value from each tuple in the list
    ids = [str(id[0]) for id in ids]
    id = input("\nWhat is the book id? ")

    
    try:
        # deletes record if provided id exists
        cursr.execute('''DELETE FROM book
        WHERE id = ?''', (id,))
        
        # displays updated records
        contents = cursr.execute('''SELECT * FROM book''')
        print(format_data(contents.fetchall()))
        
        # gives option to undo the deletion
        undo_deletion_option = input("Would you like to undo the deletion? Y/N: ")
        if undo_deletion_option == "Y" or undo_deletion_option == "y":
            db.rollback()

            # displays updated records
            contents = cursr.execute('''SELECT * FROM book''')
            print(format_data(contents.fetchall()))
        
        else:
            pass

        db.commit()
    except: 
        print("ValueError")
    

def search_books():
    '''search the database to find a specific book'''

    try:
        # provides selection for title or author search
        title_or_author = int(input("\nEnter 0 to provide a title or 1 to provide a author: "))
        title_author_selection = ["title","author"]
        title_author_selection = title_author_selection[title_or_author]
        search_crit = input(f"\nEnter the partial or full {title_author_selection} of the book: ")
        # https://www.sqlitetutorial.net/sqlite-like/#:~:text=The%20s%25%20pattern%20that%20uses,such%20as%20percent%20and%20peeper%20.
        
        # formats entry with % to search for matching words/characters 
        search_crit = f"%{search_crit}%"
        
        # searches through the records using the user-supplied words/characters
        found_book = cursr.execute(f'''SELECT * FROM book
        WHERE {title_author_selection} LIKE ?;''', (search_crit,))

        # displays the identified book
        print(found_book.fetchone())
    except:
        print("ValueError")

    
        
print("Welcome to the ebookstore database.")
while True:
    query_selection = int(input("""

    Select one of the following options: 
    1 - Enter book
    2 - Update book
    3 - Delete book
    4 - Search books
    0 - Exit

    Selection: """))

    if query_selection == 1:
        add_book_db()

    elif query_selection == 2:
        update_book()
            

    elif query_selection == 3:
        delete_book()

    elif query_selection == 4:
        search_books()

    elif query_selection == 0:
        db.close()
        print("\nGoodbye!")
        quit()
    
    else:
        print("Invalid entry.")
        exit()