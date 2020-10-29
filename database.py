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
def execute_sql_scripts(connection, scripts):
    """Execute the script in list of scripts.
    connection  - connection with database
    scripts     - script or list of scripts from 'sql_sripts.py'
                  if script require arguments use a dictionary with
                  'script' (type: string) and 'arguments' (type: tuple or string)
    
    Example 1:
        execute_sql_scripts(connection=connection, scripts=create['table_songs'])

    Example 2:
        execute_sql_scripts(
            connection  = connection,
            scripts     = {'script': create['song'], 'arguments': (song_id, band, album, nr, title)}
        )

    Example 3:
        execute_sql_scripts(
            connection  = connection,
            scripts     = [
                create['table_songs'],
                {'script': create['song'], 'arguments': (song_id, band, album, nr, title)}
            ]
        )"""

    # Convert scripts to list
    if type(scripts) in [dict, str]:
        scripts = [scripts]

    elif type(scripts) != list:
        print(f"Error: Script cannot be converted to list (must be list, set or string but not {type(scripts).__name__})")
        return None
    
    # Check scripts arguments
    for script in scripts:
        if type(script) == dict:
            ind     = scripts.index(script)
            scr     = script['script']
            arg     = script['arguments']

            if type(arg) not in [tuple, str]:
                print(f"Error: Arguments for script nr {ind} must be list or string not {type(arg).__name__}")
                return None
            
            if scr.count('?') > len(arg):
                print(f"Error: Arguments for script nr {ind} is not enough")
                return None
            elif scr.count('?') < len(arg):
                print(f"Warring: Script nr {ind} not require arguments")
                scripts[ind] = scr

    # Execute script
    if connection:
        result = list()

        for script in scripts:
            arguments = False

            if type(script) == dict:
                arguments   = script['arguments']
                script      = script['script']

            try:
                cursor = connection.cursor()

                if arguments:
                    print(f"Execute with arguments {arguments}:\n{script}\n")
                    cursor.execute(script, arguments)
                    connection.commit()
                else:
                    print(f'Execute: {script}\n')
                    cursor.execute(script)
            except sys.exc_info()[0] as error:
                print('Error:', error)
            else:
                if 'SELECT' in script:
                    result.append(cursor.fetchall())

        return result
    else:
        print("Error: Connection is lost")
        return None

#================================================================
if __name__ == '__main__':
    database_file   = "database.db"
    connection      = create_connection(database_file)

    if connection:

        result = execute_sql_scripts(
            connection  = connection,
            scripts     = [
                create['table_songs'],
                {'script': create['song'], 'arguments': (325, 'Band', 'Album', 0, 'Title')}
            ]
        )

        print('result =', result)

        #----------------
        connection.close()