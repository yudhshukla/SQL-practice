import sqlite3

#database to store flag colors, size, country, continent, symbols (weapons, people, animals, nature), year created

'''
-----------------------------------------------------------------
id | country | continent | colors | size | symbols | year created
-----------------------------------------------------------------
'''

#id : INTEGER, country : TEXT, continent : TEXT, colors : TEXT, size : TEXT, symbols : TEXT, year created : INTEGER

#create flags.db if it doesnt exist
con = sqlite3.connect("flags.db")
cur = con.cursor()

#create a table with an auto incrementing id
cur.execute("""
    CREATE TABLE IF NOT EXISTS flags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL UNIQUE, -- ensure only one flag per country
        continent TEXT NOT NULL,
        colors TEXT NOT NULL,
        size TEXT,
        symbols TEXT,
        year_created INTEGER NOT NULL
    )"""
)

#insert a few rows
cur.executemany("INSERT OR IGNORE INTO flags (country, continent, colors, size, symbols, year_created) VALUES (?, ?, ?, ?, ?, ?)", [  
    ('Mozambique', 'Africa', 'Green, black, golden-yellow, white, red', '2:3', 'Bayonet-equipped AK-47, hoe, open book', 1983),
    ('Seychelles', 'Africa', 'Blue, yellow, red, white, green', '1:2', 'None', 1996),
    ('Kiribati', 'Oceania', 'Red, yellow, white, blue', '1:2', 'Frigatebird, rising sun, ocean waves', 1979),
    ('Palau', 'Oceania', 'Light blue, yellow, white', '5:8', 'Yellow disk (full moon)', 1981),
    ('Vatican City', 'Europe', 'Yellow, white', '1:1', 'Papel tiara, crossed keys of Saint Peter', 1929)
])

con.commit()

#take user input to insert
print('\n----------------------------------------------------------------------\n')
print(' ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ Welcome to our flag database!!!!  ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')
print('\n----------------------------------------------------------------------\n')
print('Enter a new flag to add to our database:\n')
print('''There are many things you can do here! You can ADD new flags, VIEW existing flags, 
FILTER by flag attributes, UPDATE flag attributes, and DELETE flags.\n''')

while True: 
    action = input('What would you like to do first? (ADD/VIEW/FILTER/UPDATE/DELETE): \n')

    if action.lower() == 'add':
        #query user for all flag attributes
        print("\nYay! Let's add a new flag to our database! Please enter the following information: \n")
        country = input('Country: ')
        continent = input('Continent: ')
        colors = input('Colors: ')
        size = input('Size: ')
        symbols = input('Symbols: ')
        
        while True: #only allow ints for year adopted
            try:
                year_created = int(input('Year Adopted: '))
                break
            except ValueError:
                print('Please enter a valid number!\n')

        #insert new row with user's provided attributes
        cur.execute("INSERT OR IGNORE INTO flags (country, continent, colors, size, symbols, year_created) VALUES (?, ?, ?, ?, ?, ?)",
                    (country, continent, colors, size, symbols, year_created))
        con.commit()

        #query user to see updated database
        see = input('Would you like to see the updated database? (Y/N): ')
        if see.lower() == 'y' or see.lower() == 'yes':
            rows = cur.execute("SELECT * FROM flags").fetchall()
            for row in rows:
                print(row)

    elif action.lower() == 'view':
        print("\nLet's take a look at the flags in our database: \n")
        rows = cur.execute("SELECT * FROM flags").fetchall()
        for row in rows:
            print(row)

    elif action.lower() == 'filter':
        print("\nWhat flag attribute would you like to filter by? You can filter by continent, color, size, symbols, or year created. \n")
        filter_by = input('What attribute would you like to filter by? (continent/color/size/symbols/year): \n')
        
        if filter_by.lower() == 'continent':
            userContinent = input('Enter a continent to filter by: \n')
            rows = cur.execute("SELECT * FROM flags WHERE continent = ?", (userContinent,)).fetchall()
            if not rows: #check if there are any flags that match the user's filter
                print(f'Sorry, there are no flags from {userContinent} in our database yet! Maybe you can add one!!\n')
            else:
                for row in rows:
                    print(row)
            
        elif filter_by.lower() == 'color':
            userColors = input('Enter colors separated by commas (e.g., red, white): \n')
            # split the input into a clean list of words: ['red', 'white']
            colorList = [color.strip() for color in userColors.split(',')]

            # build the exact number of 'colors LIKE ?' chunks 
            conditions = []
            parameters = []

            for color in colorList:
                conditions.append('colors LIKE ?')# add a chunk to the SQL string
                parameters.append(f'%{color}%')   # add the wildcard word to our variables list

            # put chunks together with ' AND ' to make it "colors LIKE ? AND colors LIKE ?"
            whereClause = " AND ".join(conditions)

            #combine it into the final SQL command
            colorQuery = f"SELECT * FROM flags WHERE {whereClause}"

            # convert the parameters list to a tuple for sqlite
            rows = cur.execute(colorQuery, tuple(parameters)).fetchall()

            if not rows:
                print('Sorry, no flags found with those exact colors :( \n')
            else:
                for row in rows:
                    print(row)
            
        elif filter_by.lower() == 'size':
            userSize = input('Enter a size to filter by: \n')
            rows = cur.execute("SELECT * FROM flags WHERE size = ?", (userSize,)).fetchall()
            if not rows:
                print(f'Sorry, there are no flags with size {userSize} in our database yet! Maybe you can add one!!\n')
            else:
                for row in rows:
                    print(row)
        
        elif filter_by.lower() == 'symbols':
            userSymbol = input('Enter ONE symbol to search for (e.g., sun, star, moon): \n')
            
            # Wrap the word in wildcards
            search_term = f"%{userSymbol.strip()}%" 
            
            rows = cur.execute("SELECT * FROM flags WHERE symbols LIKE ?", (search_term,)).fetchall()
            
            if not rows:
                print(f'Sorry, no flags found containing "{userSymbol}" :( \n')
            else:
                for row in rows:
                    print(row)
        
        elif filter_by.lower() == 'year':
            while True:
                try:
                    userYear = int(input('Enter a year to filter by: \n'))
                    break
                except ValueError:
                    print('Please enter a valid number!\n')

            rows = cur.execute("SELECT * FROM flags WHERE year_created = ?", (userYear,)).fetchall()
            if not rows:
                print(f'Sorry, there are no flags created in {userYear} in our database yet! Maybe you can add one!!\n')
            else:
                for row in rows:
                    print(row)
        elif filter_by.lower() == 'quit':
            print('Thanks for using the flag database! Goodbye!\n')
            break

