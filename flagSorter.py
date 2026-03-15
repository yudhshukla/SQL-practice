import sqlite3

#database to store flag colors, size, country, continent, symbols (weapons, people, animals, nature), year adopted

'''
-----------------------------------------------------------------
id | country | continent | colors | size | symbols | year
-----------------------------------------------------------------
'''

#id : INTEGER, country : TEXT, continent : TEXT, colors : TEXT, size : TEXT, symbols : TEXT, year : INTEGER

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
        year INTEGER NOT NULL
    )"""
)

#list of attributes for reference
attributes = ['country', 'continent', 'colors', 'size', 'symbols', 'year']

#insert a few rows
cur.executemany("INSERT OR IGNORE INTO flags (country, continent, colors, size, symbols, year) VALUES (?, ?, ?, ?, ?, ?)", [  
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
print('''There are many things you can do here! You can \n\nADD new flags, \nVIEW existing flags, \
\nFILTER by flag attributes, \nUPDATE flag attributes, and \nDELETE flags''')

def printFlags():
    rows = cur.execute("SELECT * FROM flags").fetchall()
    print('\nID  | Country | Continent | Colors | Size | Symbols | Year Adopted\n')
    for row in rows:
        print(f'{row[0]}{' ' * (3 - len(str(row[0])))} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}')

while True: 
    action = input('\nWhat would you like to do? (ADD/VIEW/FILTER/UPDATE/DELETE): ')
    action = action.lower()
    action = action.strip()
    
    if action == 'add':
        #query user for all flag attributes
        print("\nYay! Let's add a new flag to our database! Please enter the following information: \n")
        country = input('Country: ')
        continent = input('Continent: ')
        colors = input('Colors: ')
        size = input('Size: ')
        symbols = input('Symbols: ')
        
        while True: #only allow ints for year
            try:
                year = int(input('Year Adopted: '))
                break
            except ValueError:
                print('Please enter a valid number!\n')

        #insert new row with user's provided attributes
        cur.execute("INSERT OR IGNORE INTO flags (country, continent, colors, size, symbols, year) VALUES (?, ?, ?, ?, ?, ?)",
                    (country, continent, colors, size, symbols, year))
        con.commit()

        #query user to see updated database
        see = input('Would you like to see the updated database? (Y/N): ')
        if see.lower() == 'y' or see.lower() == 'yes':
            printFlags()

    elif action == 'view':
        print("\nLet's take a look at the flags in our database:")
        printFlags()

    elif action == 'filter':
        filterBy = input('\nWhat attribute would you like to filter by? (continent/colors/size/symbols/year): ')
        filterBy = filterBy.lower()
        filterBy = filterBy.strip()
        
        while filterBy not in attributes:
            print('\nSorry, that is not a flag attribute to filter by. Please try again.')
            filterBy = input('\nWhich attribute would you like to filter by? (continent/colors/size/symbols/year): ')
            filterBy = filterBy.lower()
            filterBy = filterBy.strip()

        if filterBy.lower() == 'continent':
            userContinent = input('\nEnter a continent to filter by: ')
            rows = cur.execute("SELECT * FROM flags WHERE continent = ?", (userContinent,)).fetchall()
            if not rows: #check if there are any flags that match the user's filter
                print(f'\nSorry, there are no flags from {userContinent} in our database yet! Maybe you can add one!!')
            else:
                for row in rows:
                    print(row)
            
        elif filterBy == 'colors':
            userColors = input('\nEnter colors separated by commas (e.g., red, white): ')
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

            #combine it into the final SQL command and convert the parameters list to a tuple for sqlite
            rows = cur.execute("SELECT * FROM flags WHERE " + whereClause, tuple(parameters)).fetchall()

            if not rows:
                print('\nSorry, no flags found with those colors :( ')
            else:
                for row in rows:
                    print(row)
            
        elif filterBy == 'size':
            userSize = input('\nEnter a size to filter by: ')
            rows = cur.execute("SELECT * FROM flags WHERE size = ?", (userSize,)).fetchall()
            if not rows:
                print(f'\nSorry, there are no flags with size {userSize} in our database yet! Maybe you can add one!!')
            else:
                for row in rows:
                    print(row)
        
        elif filterBy == 'symbols':
            userSymbol = input('\nEnter ONE symbol to search for (e.g., sun, star, moon): ')
            
            # wrap the word in wildcards
            search_term = f'%{userSymbol.strip()}%'
            
            rows = cur.execute("SELECT * FROM flags WHERE symbols LIKE ?", (search_term,)).fetchall()
            
            if not rows:
                print(f'\nSorry, no flags found containing "{userSymbol}" :( ')
            else:
                for row in rows:
                    print(row)
        
        elif filterBy == 'year':
            while True:
                try:
                    userYear = int(input('\nEnter a year to filter by: '))
                    break
                except ValueError:
                    print('\nPlease enter a valid number!')

            rows = cur.execute("SELECT * FROM flags WHERE year = ?", (userYear,)).fetchall()
            if not rows:
                print(f'\nSorry, there are no flags adopted in {userYear} in our database yet! Maybe you can add one!!')
            else:
                for row in rows:
                    print(row)

    elif action == 'update':
        print('\nHere are the flags in our database:')
        printFlags()
        userUpdateFlag = input('\nWhich flag would you like to update? Please enter the country name or id: ')
        
        if type(userUpdateFlag) == int or userUpdateFlag.isdigit(): 
            userUpdateFlag = int(userUpdateFlag)
        
        row = cur.execute("SELECT * FROM flags WHERE id = ? OR country = ?", (userUpdateFlag, userUpdateFlag)).fetchone()
        while not row: 
            print(f'\nSorry, there is no flag matching "{userUpdateFlag}" in our database! Please try again.')
            userUpdateFlag = input('\nWhich flag would you like to update? Please enter the country name or id: ')
            if type(userUpdateFlag) == int or userUpdateFlag.isdigit(): 
                userUpdateFlag = int(userUpdateFlag)
            row = cur.execute("SELECT * FROM flags WHERE id = ? OR country = ?", (userUpdateFlag, userUpdateFlag)).fetchone()

        print(f'\nYou have chosen to update the flag: {row}')

        userUpdateAttribute = input('\nWhat attribute of this flag would you like to update? (continent/colors/size/symbols/year): ')
        userUpdateAttribute = userUpdateAttribute.lower()
        userUpdateAttribute = userUpdateAttribute.strip()

        while userUpdateAttribute not in attributes:
            print('\nSorry, that is not a valid flag attribute. Please try again.')
            userUpdateAttribute = input('\nWhat attribute of this flag would you like to update? (continent/colors/size/symbols/year): ')

        userUpdateValue = input(f'\nEnter the new value for {userUpdateAttribute}: ')

        if type(userUpdateFlag) == int:
            updateQuery = "UPDATE flags SET " + userUpdateAttribute + " = ? WHERE id = ?"
            cur.execute(updateQuery, (userUpdateValue, userUpdateFlag))
        else:
            updateQuery = "UPDATE flags SET " + userUpdateAttribute + " = ? WHERE country = ?"
            cur.execute(updateQuery, (userUpdateValue, userUpdateFlag))
        
        con.commit()

        print('\nFlag updated successfully!')
    
    elif action == 'delete':
        print('\nHere are the flags in our database:')
        printFlags()
        userDeleteFlag = input('\nWhich flag would you like to delete? Please enter the country name or id: ')
        
        row = cur.execute("SELECT * FROM flags WHERE id = ? OR country = ?", (userDeleteFlag, userDeleteFlag)).fetchone()
        while not row: 
            print(f'\nSorry, there is no flag matching "{userDeleteFlag}" in our database! Please try again.')
            userDeleteFlag = input('\nWhich flag would you like to delete? Please enter the country name or id: ')
            if type(userDeleteFlag) == int or userDeleteFlag.isdigit(): 
                userDeleteFlag = int(userDeleteFlag)
            row = cur.execute("SELECT * FROM flags WHERE id = ? OR country = ?", (userDeleteFlag, userDeleteFlag)).fetchone()
            
        print(f'\nYou have chosen to delete the flag: {row}')
        confirmDelete = input('\nAre you sure you want to delete this flag? (Y/N): ')
        if confirmDelete.lower() != 'y':
            print('\nFlag deletion canceled.')
            continue

        if type(userDeleteFlag) == int or userDeleteFlag.isdigit(): 
            userDeleteFlag = int(userDeleteFlag)
            deleteQuery = "DELETE FROM flags WHERE id = ?"
            cur.execute(deleteQuery, (userDeleteFlag,))
        else:
            deleteQuery = "DELETE FROM flags WHERE country = ?"
            cur.execute(deleteQuery, (userDeleteFlag,))
        
        con.commit()

        print('\nFlag deleted successfully!')

    elif action == 'quit':
        print('Thanks for using the flag database! Goodbye!\n')
        break

    else:
        print('\nSorry, that is not a valid action. Please try again.')

con.close()