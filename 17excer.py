import sqlite3
import pandas as pd

# Connect to the SQLite database
def connect_to_db(db_path):
    return sqlite3.connect(db_path)

# Function to query and display authors' last names in descending order
def get_authors_last_names(cursor):
    cursor.execute("SELECT last FROM authors ORDER BY last DESC;")
    return cursor.fetchall()

# Function to query and display book titles in ascending order
def get_book_titles(cursor):
    cursor.execute("SELECT title FROM titles ORDER BY title ASC;")
    return cursor.fetchall()

# Function to query books for a specific author
# Includes title, copyright, and ISBN ordered alphabetically by title
def get_books_by_author(cursor, last_name):
    cursor.execute(
        """
        SELECT titles.title, titles.copyright, titles.isbn
        FROM authors
        JOIN author_ISBN ON authors.id = author_ISBN.id
        JOIN titles ON author_ISBN.isbn = titles.isbn
        WHERE authors.last = ?
        ORDER BY titles.title ASC;
        """,
        (last_name,)
    )
    return cursor.fetchall()

# Function to insert a new author
def insert_author(cursor, first_name, last_name):
    cursor.execute("INSERT INTO authors (first, last) VALUES (?, ?);", (first_name, last_name))

# Function to insert a new book and associate it with an author
def insert_book(cursor, isbn, title, edition, copyright, author_id):
    cursor.execute(
        "INSERT INTO titles (isbn, title, edition, copyright) VALUES (?, ?, ?, ?);",
        (isbn, title, edition, copyright),
    )
    cursor.execute(
        "INSERT INTO author_ISBN (id, isbn) VALUES (?, ?);",
        (author_id, isbn),
    )

# Function to display data in tabular format
def display_data_as_table(data, column_names):
    df = pd.DataFrame(data, columns=column_names)
    print(df)
    return df

if __name__ == "__main__":
    # Database path
    db_path = r"C:\\Users\\Jessi\\Downloads\\ch17\\books.db"  # Updated path to the correct location

    # Connect to the database
    conn = connect_to_db(db_path)
    cursor = conn.cursor()

    # 1. Select all authors' last names in descending order
    authors_last_names = get_authors_last_names(cursor)
    print("Authors' Last Names in Descending Order:")
    for last_name in authors_last_names:
        print(last_name[0])

    # 2. Select all book titles in ascending order
    book_titles = get_book_titles(cursor)
    print("\nBook Titles in Ascending Order:")
    for title in book_titles:
        print(title[0])

    # 3. Select all books for a specific author (e.g., Deitel)
    author_books = get_books_by_author(cursor, "Deitel")
    print("\nBooks by Deitel:")
    column_names = ["Title", "Copyright", "ISBN"]
    df_books = display_data_as_table(author_books, column_names)

    # 4. Insert a new author
    new_author_first = "Jane"
    new_author_last = "Smith"
    insert_author(cursor, new_author_first, new_author_last)
    conn.commit()
    print(f"\nInserted new author: {new_author_first} {new_author_last}")

    # 5. Insert a new title for the new author
    new_isbn = "1234567890"
    new_title = "Advanced Python Programming"
    new_edition = 1
    new_copyright = "2024"
    cursor.execute("SELECT id FROM authors WHERE last = ?;", (new_author_last,))
    new_author_id = cursor.fetchone()[0]
    insert_book(cursor, new_isbn, new_title, new_edition, new_copyright, new_author_id)
    conn.commit()
    print(f"\nInserted new book: {new_title} for author {new_author_first} {new_author_last}")

    # Close the database connection
    conn.close()
