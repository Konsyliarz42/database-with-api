import sqlite3, sys, os

from sql_sripts import create, read, update, delete

#--------------------------------
def create_connection(db_file=False):
    """Create a database connection to a SQLite database.
    db_file - file of database, if this argument is not defined
              the function create database in memory"""

    connection = False

    if not db_file:
        db_file = ":memory:"
    else:
        if not os.path.exists(db_file):
            print(f"Create {db_file}...")

    try:
        connection = sqlite3.connect(db_file)
    except sys.exc_info()[0] as error:
        print('Error:', error)
    else:
        if db_file != ":memory:":
            print(f"Connect with {db_file}!\n")
        else:
            print("Connected!\n")

    return connection

#--------------------------------
def add_song(connection, song):
    """Add song to table 'songs' in database.
    connection  - connection with database
    song        - tuple with information about song
                  (song_id, band, album, nr, title)"""

    script  = create['song']
    scr     = script
    son     = list(song)
    son.reverse()
    
    while '?' in scr:
        scr = scr.replace('?', str(son[scr.count('?') - 1]), 1)

    if connection:
        try:
            cursor = connection.cursor()

            print(f"Execute:{scr}\n")
            cursor.execute(script, song)
        except sys.exc_info()[0] as error:
            print('Error:', error)
        else:
            connection.commit()
            return cursor.lastrowid
    else:
        print("Error: Connection is lost")

#--------------------------------
def execute_sql_scripts(connection, scripts):
    """Execute the script in list of scripts.
    connection  - connection with database
    scripts     - list of scripts from 'sql_sripts.py'"""

    if type(scripts) == str:
        scripts = [scripts]
    else:
        print("Error: Argument 'scripts' cannot be converted to list")
        return None

    if connection:
        for script in scripts:
            try:
                cursor = connection.cursor()

                print(f"Execute:{script}\n")
                cursor.execute(script)
            except sys.exc_info()[0] as error:
                print('Error:', error)
    else:
        print("Error: Connection is lost")

#================================================================
if __name__ == '__main__':
    database_file   = "database.db"
    connection      = create_connection(database_file)

    if connection:
        execute_sql_scripts(connection, create['table_songs'])
        add_song(connection, ('uuid', 'Nachtblut', 'Vanitas', 4, 'Das Puppenhaus'))

        #----------------
        connection.close()