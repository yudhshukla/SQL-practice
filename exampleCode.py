"""
Some example code for SQLite
-------------------------------------------------------------
SQLite is serverless and can run locally, but it loses out on the ability
to do more than one write operation at a time, so it can *sometimes* be slow.  
This is typically not a major problem for projects unless you're serving many 
users or dealing with very large datasets that require regular updates.
-------------------------------------------------------------
"""

import sqlite3

# Connect (creates books.db if it doesn't exist)
con = sqlite3.connect("books.db")
cur = con.cursor()

# Create table with an auto-incrementing id
cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id      INTEGER PRIMARY KEY,
        title   TEXT NOT NULL,
        author  TEXT NOT NULL,
        rating  INTEGER
    )
""")

# Insert rows 
# (PERSISTANCE WARNING! Watch out for adding duplicate books with new IDs!)
cur.executemany("INSERT INTO books (title, author, rating) VALUES (?, ?, ?)", [
    ('Dune', 'Herbert', 5),
    ('Neuromancer', 'Gibson', 4),
    ('Foundation', 'Asimov', 5),
    ('Snow Crash', 'Stephenson', 3),
])

con.commit()  # <-- persists the writes to disk

# Get every row
print("All rows:")
rows = cur.execute("SELECT * FROM books").fetchall()
for row in rows:
    print(row)

# Query
print("\nRows with rating >= 4:")
rows = cur.execute("SELECT * FROM books WHERE rating >= 4 ORDER BY author").fetchall()
for row in rows:
    print(row)

# Another Query
print("\nFind just one author:")
rows = cur.execute("SELECT * FROM books WHERE author = 'Herbert'").fetchall()
for row in rows:
    print(row)

# The previous query ran in O(N), as we might expect
# ...but if we explicitly do the following, we can make that query run in O(logN)
cur.execute("CREATE INDEX idx_author ON books (author)")
con.commit()

# This creates a new binary tree keyed on the author

print("\nFind just one author, but now it's indexed:")
rows = cur.execute("SELECT * FROM books WHERE author = 'Herbert'").fetchall()
for row in rows:
    print(row)

# The downside here is that every insert, update, or delete must update each 
# index's binary tree, which is O(logN) each time.  This is why we don't 
# just index on everything. 

# Aggregation
print("\nAverage rating:")
print(cur.execute("SELECT AVG(rating) FROM books").fetchone()) #note fetchONE
print("\nNumber of books by each author:")
print(cur.execute("SELECT author, COUNT(*) FROM books GROUP BY author").fetchall())

# Update
print("\nUpdate and check  the rating for Dune:")
cur.execute("UPDATE books SET rating = 4 WHERE title = 'Dune'")
print(cur.execute("SELECT * FROM books WHERE title = 'Dune'").fetchone())

# Delete
print("\nDelete sub-4 ratings and check what's left:")
cur.execute("DELETE FROM books WHERE rating < 4")
print(cur.execute("SELECT * FROM books").fetchall())

# Note that this is subtly different than the query we ran before in that it will
# omit any rows that have a NULL author, (IF such rows existed):
print(cur.execute("SELECT author, COUNT(author) FROM books GROUP BY author").fetchall())

# NULL is sort of like None in Python, but it's more similar to "Unknown"
# "NULL is contagious"
print("\nSome NULL examples:")
print(cur.execute("SELECT 5 + NULL").fetchall())
print(cur.execute("SELECT NULL = NULL").fetchall())

# This will NOT find books with no author
print(cur.execute("SELECT * FROM books WHERE author = NULL").fetchall())

# You MUST use this instead
print(cur.execute("SELECT * FROM books WHERE author IS NULL").fetchall())

# Close the connection (Super important to do this)
con.close()



