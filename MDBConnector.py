import mariadb



class Database:

    class Table:
        def __init__(self, name, columns_list):
            self.num_of_columns = 1
            self.values_pattern = ''
            self.columns = columns_list




    def __init__(self, user, password, host, port, database):
        """Initialize and connect to server

        Arguments:
            user {string} -- username \n
            password {string} -- password \n
            host {string} -- host (localhost) \n
            port {int} -- port (3306) \n
            database {string} -- database name \n
        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.tables = list()

        try:
            self.connector = mariadb.connect(user=str(user[0]), password=str(password[0]), host=str(host[0]), port=int(port[0]), database=str(database))
            self.cursor = self.connector.cursor()
        except mariadb.Error as err:
            print(err)
            self.__del__()




    def __del__(self):
        """Destructor
        """
        self.connector.close()
    



    def get_tables(self):
        """Get the names of the existing tables 
        """
        self.cursor.execute("SHOW TABLES")
        self.tables = list()
        for row in self.cursor:
            self.tables.append(row[0])
        




    def parse_column_definition(self, columns):
        """Make column definition string from list

        Arguments:
            columns {list} -- list that contains the name of the column and its definition

        Returns:
            string -- final string to be put in the CREATE TABLE query

        """
        final_string = str()

        final_string = columns[0][0] + ' ' + columns[0][1]

        for col in range(1, len(columns)):
            final_string += ', '
            final_string += columns[col][0] + ' ' + columns[col][1]
        
        return final_string
    




    def new_table(self, opperation ,table_name, columns = None):
        """Create new table in database

        Arguments:
            opperation {char} -- Type of operation to perform: 'i' (if not exists) 'r' (replace) \n
            table_name {string} -- Name of the new table
        """
        if columns is None:
            columns = [['id', 'INT PRIMARY KEY NOT NULL AUTO_INCREMENT']]

        self.tables.append(self.Table(table_name, columns))

        final_string = self.parse_column_definition(columns)

        match opperation:
            case 'r':
                self.cursor.execute(f"CREATE OR REPLACE TABLE {table_name} ({final_string});")
            case 'i':
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({final_string});")
            case _:
                self.cursor.execute(f"CREATE TABLE {table_name} ({final_string});")
        self.tables.append(table_name)




    def select_table(self, table_name):
        """Selects a table in the database

        Arguments:
            table_name {string} -- Table to be selected
        """

        if not table_name in self.tables:
            print(f"There isn't a table called '{table_name}' in the database")
            return
        self.selected_table = table_name





    def add_column(self, column, after = None):
        """Adds column to selected table. A table must be selected before calling

        Arguments:
            column_name {string} -- Name of the new column \n
            column_definition {list} -- Definition of the new column \n

        Keyword Arguments:
            after {string} -- Insert after this column. If None inserts at the end (default: {None})
        """

        column_string = self.parse_column_definition(column)

        for col in column:
            self.columns.append(col)

        if self.selected_table is None:
            print("Select a table before adding a column")
        elif after is None:
            self.cursor.execute(f"ALTER TABLE {self.selected_table} ADD COLUMN IF NOT EXISTS {column_string}")
        else:
            self.cursor.execute(f"ALTER TABLE {self.selected_table} ADD COLUMN IF NOT EXISTS {column_string} AFTER {after}")
        




    def delete_column(self, column_name):
        """Deletes column of a table. Does not raise error if column doesn't exist. Table must be selected beforehand. You can't delete the only column in a table

        Arguments:
            column_name {string} -- name of the column to delete
        """
        if self.selected_table is None:
            print("Select a table before deleting a column")
        else:
            self.cursor.execute(f"select count(*) from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.selected_table}'")
            if list(self.cursor)[0][0] == 1:
                print("You can't delete the only column in the table")
            else:
                self.cursor.execute(f"ALTER TABLE {self.selected_table} DROP COLUMN IF EXISTS {column_name}")





    def insert_data(self):
        if self.selected_table is None:
            print("Select a table before inserting data")

        values_pattern = self.columns[0][0]

        for i in range(1, len(self.columns)):
            values_pattern += ', '
            values_pattern += self.columns[i][0]



