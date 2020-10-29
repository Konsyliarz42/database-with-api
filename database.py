import sqlite3, sys

#================================================================
class SQLiteDatabase():
    def __init__(self, file=None):
        self.connection = False
        self.cursor     = None

        if file:
            self.file = file
        else:
            self.file=":memory:"

    #--------------------------------
    def __del__(self):
        if self.connection:
            self.connection.close()
            self.cursor = None

    #--------------------------------
    def __repr__(self):
        return f"SQLite database in {self.file}"

    #--------------------------------
    def connect(self):
        """Activate connection with database"""

        try:
            print("Conection to SQLite database...", end=' ')
            self.connection = sqlite3.connect(self.file)
            self.cursor     = self.connection.cursor()
        except sys.exc_info()[0] as error:
            print('Error:', error)
        else:
            print("Connected!\n")
        finally:
            return self.connection
    
    #--------------------------------
    def create_table(self, table_name, *, primary_key='id', **columns):
        """Create a table in database.
        Requirement:
            table_name  - name of a table

        Optional:
            primary_key - column who has primary key
            columns     - variable which are names of column and
                          their values which have a type and optional values
                          
        Function require active connection to database!
        You can activate connection using connect() function before this function"""

        columns_name = ''

        # Add id column if not exist
        if 'id' not in columns:
            columns_name = '\tid integer'

            if primary_key == 'id':
                columns_name += " PRIMARY KEY"

        # Create script
        for col_name, col_type in zip(columns.keys(), columns.values()):
            if columns_name:
                columns_name += ',\n\t'
            else:
                columns_name += '\t'

            columns_name += f"{col_name} {col_type.lower()}"

            if col_name == primary_key:
                columns_name += " PRIMARY KEY"

        script = f"""
    -- {table_name} table
    CREATE TABLE IF NOT EXISTS {table_name}
    (
    {columns_name}
    );"""

        # Execute script
        try:
            print(f"Execute:{script}\n")
            self.cursor.execute(script)
        except sys.exc_info()[0] as error:
            print('Error:', error)

    #--------------------------------
    def add_to_table(self, table_name, **parameters):
        """Add to table row from tuple 'parameters'.
        Requirement:
            parameters  - variables which are values new row a table
            table_name  - name of a table"""

        # Check parameters
        if not parameters:
            raise TypeError("add_to_table() missing 1 required keyword-only argument: 'parameters'")        

        # Create script
        names_parameters    = ', '.join([str(name) for name in parameters.keys()]) 
        values_parameters   = tuple([value for value in parameters.values()])
        values              = '?, '*len(values_parameters)

        script = f"""
    INSERT INTO {table_name}({names_parameters})
        VALUES({values[:-2]})"""

        # Execute script
        try:
            print(f"Execute with parameters {values_parameters}:\n{script}\n")
            self.cursor.execute(script, values_parameters)
            self.connection.commit()
        except sys.exc_info()[0] as error:
            print('Error:', error)

    #--------------------------------    
    def select_from_table(self, table_name, **parameters):
        """Return rows which parameters.
        Requirement:
            table_name  - name of a table

        Optional:
            parameters  - conditions of search.
                          
        Return:
            List of result of search."""

        # Create script
        result      = []
        values      = tuple([value for value in parameters.values()])
        conditions  = '=? AND '.join([name for name in parameters.keys()]) + '=?'
        

        script = f"""
    SELECT * FROM {table_name}"""

        if parameters:
            script  += f" WHERE {conditions}"
            msg     = f"Execute with parameters {values}:\n{script}\n"
        else:
            msg = f"Execute:\n{script}\n"

        # Execute script
        try:
            print(msg)
            self.cursor.execute(script, values)
            result = self.cursor.fetchall()
        except sys.exc_info()[0] as error:
            print('Error:', error)
        finally:
            return result

    #--------------------------------
    def update_row(self, table_name, primary_key, **parameters):
        """Update a row in table.
        Requirement:
            table_name  - name of a table
            primary_key - dict with 'name' and 'value' of primary key
            
        Optiona:
            parameters  - variables of new values in rows, must be min one"""

        # Check parameters
        if not parameters:
            raise TypeError("update_row() missing 1 required keyword-only argument: 'parameters'")

        # Create script
        columns = '\t    ' + '=?,\n\t    '.join([name for name in parameters.keys()]) + '=?'
        values  = [primary_key['value']] + [value for value in parameters.values()]
        values  = tuple(values)
        key     = primary_key['name']

        script = f"""
    UPDATE {table_name}
        SET\n{columns}
        WHERE {key}=?"""

        # Execute script
        try:
            print(f"Execute with parameters {values}:{script}\n")
            self.cursor.execute(script, values)
            self.connection.commit()
        except sys.exc_info()[0] as error:
            print('Error:', error)

    #--------------------------------
    def delete(self, table_name, **parameters):
        """Remove row in table.
        Requirement:
            table_name  - name of a table
            
        Optiona:
            parameters  - conditions of removing"""

        # Create script
        script  = f"""
    DELETE FROM {table_name}"""

        if parameters:
            conditions  = '=? AND '.join([name for name in parameters.keys()]) + '=?'
            values      = tuple([value for value in parameters.values()])
            script      += f" WHERE {conditions}"

        # Execute script
        try:
            if parameters:
                print(f"Execute with parameters {values}:\n{script}\n")
                self.cursor.execute(script, values)
            else:
                print(f"Execute:\n{script}\n")
                self.cursor.execute(script)

            self.connection.commit()
        except sys.exc_info()[0] as error:
            print('Error:', error)

#================================================================
if __name__ == '__main__':
    database = SQLiteDatabase(file="")

    print(database)
    connection = database.connect()

    database.create_table(
        table_name='songs',
        id='integer',
        song_id='integer',
        band='text',
        album='text',
        nr='integer',
        title='text'
    )

    database.add_to_table(
        table_name='songs',
        song_id=123456789,
        band='Band',
        album='Album',
        nr=0,
        title='Title'
    )

    result = database.select_from_table(
        table_name='songs',
        id=1
    )
    print("Select result:", result, '\n')

    database.update_row(
        table_name='songs',
        primary_key={'name':'id', 'value':1},
        song_id=123456789,
        album='Album',
    )

    database.delete(
        table_name='songs',
        song_id=123456789
    )

    database.__del__()